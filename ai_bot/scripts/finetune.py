# scripts/finetune.py

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

# --- Configurations ---
MODEL_PATH = "C:/huggingface/models/BharatGPT-3B-Indic"
DATA_PATH = "C:/Users/krish/Downloads/ai_bot/ai_bot/data/finetuning_dataset.json"
OUTPUT_DIR = "./finetuned_model"
MAX_LENGTH = 256
BATCH_SIZE = 1
GRAD_ACCUM = 8
EPOCHS = 1  # you can increase if needed

# --- Load Dataset ---
dataset = load_dataset("json", data_files=DATA_PATH)
train_dataset = dataset["train"]

# --- Load Tokenizer ---
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token

# --- Tokenization Function ---
def tokenize_fn(examples):
    # examples is a dict of lists
    inputs = [
        f"{instr}\n{resp}"
        for instr, resp in zip(examples["instruction"], examples["response"])
    ]
    model_inputs = tokenizer(
        inputs,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
    )
    return model_inputs

# Map tokenization
train_dataset = train_dataset.map(tokenize_fn, batched=True, remove_columns=train_dataset.column_names)

# --- Load Model in 4-bit ---
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    load_in_4bit=True,
    device_map="auto",
)

# --- Apply LoRA ---
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# --- Data Collator ---
data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

# --- Training Arguments ---
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    warmup_steps=50,
    max_steps=1000,  # can increase later
    learning_rate=2e-4,
    fp16=True,
    logging_steps=20,
    save_strategy="steps",
    save_steps=200,
    save_total_limit=2,
    report_to="none",
)

# --- Trainer ---
trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    args=training_args,
)

# --- Train ---
print("INFO:root:Starting fine-tuning...")
trainer.train()
print("INFO:root:Fine-tuning complete!")
