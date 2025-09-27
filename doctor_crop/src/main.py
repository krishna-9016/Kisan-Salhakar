import io
import os
import json
from json.decoder import JSONDecodeError
import torch
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from torchvision import transforms
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# Import our custom model creation function
from .model import create_model


# --- 1. Application Setup ---
load_dotenv()

app = FastAPI(title="Crop Doctor API")

# --- 2. Model and Mappings Loading ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure the Gemini API
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBTWgtSyVa6f87hF_Qgv-YnLzMNGOq-jqA"
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    genai.configure(api_key=GEMINI_API_KEY)

    # Create the actual model object
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    print("--- Gemini API configured successfully ---")
except Exception as e:
    print(f"ERROR: Could not configure Gemini API: {e}")
    gemini_model = None



# Define paths (relative to the project root)
MODEL_PATH = 'best_crop_doctor_model.pth'
DATA_DIR = 'processed'

# Set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the class mappings
try:
    train_df = pd.read_parquet(f'{DATA_DIR}/train.parquet')
    class_to_idx = {label: i for i, label in enumerate(train_df['label'].unique())}
    idx_to_class = {i: label for label, i in class_to_idx.items()}
    num_classes = len(class_to_idx)
except FileNotFoundError:
    print(f"ERROR: Could not find mapping file at {DATA_DIR}/train.parquet. API will not work.")
    idx_to_class = {}
    num_classes = 38  # Fallback

# Load the model
model = create_model(num_classes=num_classes, pretrained=False)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

print("--- PyTorch model and mappings loaded successfully ---")

# --- 3. API Endpoints ---

@app.post("/diagnose")
async def diagnose_disease(file: UploadFile = File(...)):
    """
    Receives an image file, makes a prediction, and returns the result.
    """
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, top_idx = torch.max(probabilities, 0)

    class_name = idx_to_class.get(top_idx.item(), "Unknown")
    confidence = top_prob.item()

    # Correct extraction logic for disease name
    try:
        disease_full_name = class_name.split('___')[1].replace('_', ' ')
    except Exception:
        disease_full_name = class_name.replace('_', ' ')  # Fallback

    return {
        "disease": disease_full_name,
        "confidence": f"{confidence * 100:.2f}%"
    }

# Pydantic model for the request body
class PrecautionRequest(BaseModel):
    disease: str

# Endpoint to get precautions from Gemini
@app.post("/precautions")
async def get_precautions(request: PrecautionRequest):
    """
    Receives a disease name and returns structured prevention/treatment measures from Gemini.
    """
    if not gemini_model:
        return {"error": "Gemini API not configured"}

    disease_name = request.disease

    prompt = (
        "You are an agricultural expert AI. Your task is to provide information about a plant disease in a structured JSON format."
        f"The plant disease is: '{disease_name}'."
        "\n\n"
        "Respond with ONLY a valid JSON object following this exact schema:"
        '{\n'
        '  "disease_name": "The common name of the disease",\n'
        '  "symptoms_summary": "A brief, one-to-two sentence summary of the main symptoms.",\n'
        '  "prevention": [\n'
        '    "A concise, actionable prevention tip.",\n'
        '    "Another concise, actionable prevention tip."\n'
        '  ],\n'
        '  "treatment": {\n'
        '    "organic_methods": [\n'
        '      "An actionable organic or cultural treatment method."\n'
        '    ],\n'
        '    "chemical_methods": [\n'
        '      "An actionable chemical treatment method (mention active ingredients if possible)."\n'
        '    ]\n'
        '  }\n'
        '}'
        "\n\n"
        "Do not include any text, explanation, or markdown formatting before or after the JSON object."
        "If the provided name is not a recognizable plant disease, return a JSON object with an 'error' key, like this: {\"error\": \"Disease not recognized\"}."
    )

    try:
        response = gemini_model.generate_content(prompt)

        cleaned_text = response.text.strip().replace("json", "").replace("```", "").strip()


        data = json.loads(cleaned_text)
        return data

    except JSONDecodeError:
        print(f"Error: Gemini API did not return valid JSON. Response:\n{response.text}")
        return {"error": "Failed to parse precautions from the generative model. The model returned a non-JSON response."}
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {"error": "Failed to get precautions from the generative model."}
