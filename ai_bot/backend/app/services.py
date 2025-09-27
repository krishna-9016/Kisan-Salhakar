# backend/app/services.py

import os
import logging
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core import exceptions as g_exceptions  # 👈 import Google exceptions

# --- Global variable for the Gemini model ---
gemini_model = None
chat_session = None

SYSTEM_INSTRUCTION = """ ... same as before ... """

def configure_gemini():
    global gemini_model, chat_session
    if gemini_model is None:
        logging.info("Configuring Gemini Pro model...")
        try:
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables.")
            genai.configure(api_key=api_key)
            gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            
            chat_session = gemini_model.start_chat(history=[
                {'role': 'user', 'parts': [SYSTEM_INSTRUCTION]},
                {'role': 'model', 'parts': ["ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ AI ਖੇਤੀਬਾੜੀ ਸਲਾਹਕਾਰ ਹਾਂ..."]},
            ])
            logging.info("Gemini Pro model configured and chat session started.")
        except Exception as e:
            logging.critical(f"Failed to configure Gemini: {e}")
            raise

class GeminiService:
    def process_query(self, query: str) -> str:
        if not chat_session:
            raise RuntimeError("Gemini chat session is not initialized.")
        
        try:
            logging.info(f"Sending query to Gemini: {query}")
            response = chat_session.send_message(query)
            return response.text
        
        except g_exceptions.ResourceExhausted as e:  # 👈 handle quota exceeded
            logging.error("Gemini quota exceeded.")
            return (
                "⚠️ ਤੁਹਾਡੀ ਮੁਫ਼ਤ ਕੋਟਾ ਸੀਮਾ ਪੂਰੀ ਹੋ ਗਈ ਹੈ। "
                "ਕਿਰਪਾ ਕਰਕੇ ਕੁਝ ਸਮਾਂ ਰੁੱਕੋ ਜਾਂ ਉੱਚੀ ਯੋਜਨਾ 'ਤੇ ਅਪਗ੍ਰੇਡ ਕਰੋ।\n"
                "(Your free quota is exhausted. Please wait or upgrade your plan.)"
            )
        
        except Exception as e:
            logging.error(f"Error communicating with Gemini: {e}")
            logging.error(traceback.format_exc())
            return "ਮਾਫ ਕਰਨਾ, ਤਕਨੀਕੀ ਖਰਾਬੀ ਕਾਰਨ ਮੈਂ ਜਵਾਬ ਨਹੀਂ ਦੇ ਸਕਦਾ।"

gemini_service = GeminiService()
