# scripts/ingest_data.py

import os
import faiss
import numpy as np
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
import logging

# --- Configuration ---
# Set up logging to provide progress and error information.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from a.env file. This is good practice for managing configuration.
load_dotenv()
AI_BOT_DIR = Path(__file__).resolve().parent.parent

# Define the path to your knowledge base documents
KNOWLEDGE_BASE_DIR = AI_BOT_DIR / "data" / "knowledge_base"
# Define paths for data sources and storage. Using Path objects makes path manipulation safer and cross-platform.

VECTOR_STORE_DIR = AI_BOT_DIR / "vector_store"
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "faiss_index.bin"
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# --- Core Functions ---

from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load_documents(directory_path: Path):
    docs = []
    for file in directory_path.glob("**/*"):
        if file.suffix == ".pdf":
            loader = PyPDFLoader(str(file))
        elif file.suffix == ".txt":
            loader = TextLoader(str(file), encoding="utf-8")
        else:
            continue
        docs.extend(loader.load())
    return docs

def split_text_into_chunks(documents: list):
    """
    Splits the loaded documents into smaller chunks for effective processing by the LLM.
    RecursiveCharacterTextSplitter tries to keep related text together.
    
    Args:
        documents (list): A list of document objects.
        
    Returns:
        list: A list of text chunks (strings).
    """
    logging.info("Splitting documents into chunks...")
    # This text splitter is configured to create chunks of up to 1024 characters
    # with an overlap of 128 characters. The overlap helps maintain context between chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    chunks = text_splitter.split_documents(documents)
    logging.info(f"Split documents into {len(chunks)} chunks.")
    return chunks

def create_embeddings(model_name: str):
    """
    Initializes and returns a HuggingFace embedding model with GPU support if available.
    """
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Initializing embedding model: {model_name} on {device.upper()}")
    
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': False}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings


def build_and_save_faiss_index(chunks: list, embeddings_model):
    """
    Creates embeddings for all text chunks and builds a FAISS index for fast similarity search.
    The index is then saved to disk.
    
    Args:
        chunks (list): A list of document chunks.
        embeddings_model: The initialized embedding model.
    """
    if not chunks:
        logging.warning("No chunks to process. Skipping FAISS index creation.")
        return

    logging.info("Generating embeddings for all text chunks. This may take a while...")
    # Extract the text content from each chunk object.
    chunk_texts = [chunk.page_content for chunk in chunks]
    
    # Generate embeddings in batches for efficiency.
    embeddings_vectors = embeddings_model.embed_documents(chunk_texts)
    
    # Convert the list of vectors to a NumPy array for FAISS.
    embeddings_np = np.array(embeddings_vectors).astype('float32')
    
    # The dimension of the vectors is the second element of the shape tuple.
    d = embeddings_np.shape[1] # <--- THE FIX IS HERE
    
    # We use IndexFlatL2, a basic but effective index type for exact nearest neighbor search.
    index = faiss.IndexFlatL2(d)
    index.add(embeddings_np)
    
    logging.info(f"FAISS index built successfully with {index.ntotal} vectors.")
    
    # Ensure the target directory exists before trying to save the file.
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save the index to a binary file.
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    logging.info(f"FAISS index saved to: {FAISS_INDEX_PATH}")
    
    # It's also critical to save the mapping from index ID to the original text chunk.
    # We'll save the chunks themselves in a simple way for this prototype.
    # A more robust solution might use a key-value store or a database.
    import pickle
    with open(VECTOR_STORE_DIR / "chunks.pkl", "wb") as f:
        pickle.dump(chunk_texts, f)
    logging.info(f"Text chunks saved to: {VECTOR_STORE_DIR / 'chunks.pkl'}")

def main():
    """
    The main function to orchestrate the entire data ingestion pipeline.
    """
    logging.info("Starting data ingestion pipeline...")
    
    # Step 1: Load documents from the knowledge base directory.
    documents = load_documents(KNOWLEDGE_BASE_DIR)
    if not documents:
        logging.error("No documents were loaded. Aborting pipeline.")
        return
        
    # Step 2: Split the documents into manageable chunks.
    chunks = split_text_into_chunks(documents)
    
    # Step 3: Initialize the embedding model.
    embeddings_model = create_embeddings(EMBEDDING_MODEL_NAME)
    
    # Step 4: Build the FAISS index from the chunks and save it.
    build_and_save_faiss_index(chunks, embeddings_model)
    
    logging.info("Data ingestion pipeline completed successfully.")

if __name__ == "__main__":
    main()