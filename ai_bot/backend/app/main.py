# backend/app/main.py

import logging
import traceback
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
from io import BytesIO

# Import your models and the SIMPLIFIED services
from .models import QueryRequest, ChatResponse
from .services import gemini_service, configure_gemini

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- FastAPI App ---
app = FastAPI(
    title="Punjabi Farmer Advisory AI (Direct Gemini)",
    description="An AI-powered conversational agent for agricultural advice in Punjabi, powered directly by Google Gemini.",
    version="2.0.0"
)

# --- CORS Middleware (Unchanged) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic model for TTS (Unchanged) ---
class TTSRequest(BaseModel):
    text: str
    lang: str = "pa"

# --- SIMPLIFIED: Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    Configure the Gemini API client on startup.
    """
    logging.info("Application starting up...")
    try:
        configure_gemini()
        logging.info("Gemini service configured. Application is ready.")
    except Exception as e:
        logging.critical(f"Failed to initialize services on startup: {e}")
        logging.critical(traceback.format_exc())

# --- Health Check Endpoint (Unchanged) ---
@app.get("/", tags=["Health Check"])
async def read_root():
    return {"status": "ok", "message": "Welcome to the Punjabi Farmer Advisory AI API (Direct Gemini)"}

# --- MODIFIED: Chat Endpoint ---
@app.post("/chat", response_model=ChatResponse, tags=["Conversational AI"])
async def chat_endpoint(request: QueryRequest):
    logging.info(f"Received query: {request.query}")
    if not request.query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty."
        )
    try:
        # The service now returns only the answer string
        answer = gemini_service.process_query(request.query)
        
        # Return the answer with an empty context list to match the Pydantic model
        return ChatResponse(
            answer=answer,
            retrieved_context=[] 
        )
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred. Please try again later."
        )

# --- Text-to-Speech Endpoint (Unchanged) ---
@app.post("/synthesize-speech", tags=["Utilities"])
async def synthesize_speech(request: TTSRequest):
    logging.info(f"Received TTS request for lang '{request.lang}': '{request.text[:50]}...'")
    if not request.text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty."
        )
    try:
        tts = gTTS(text=request.text, lang=request.lang)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return StreamingResponse(mp3_fp, media_type="audio/mpeg")
    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate speech."
        )