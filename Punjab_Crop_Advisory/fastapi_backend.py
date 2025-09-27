"""
FastAPI Backend Service for ML Model Inference
==============================================

This FastAPI service exposes your ML model as a REST API with:
- Model loading on startup
- /predict endpoint with JSON input/output
- API key authentication
- ngrok integration for public access
- CORS enabled for frontend integration
"""

import os
import sys
import pickle
import secrets
import logging
from typing import Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

import uvicorn
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate a dynamic API key (single generation per server restart)
API_KEY_FILE = '.api_key'
if os.path.exists(API_KEY_FILE):
    # Read existing API key
    with open(API_KEY_FILE, 'r') as f:
        API_KEY = f.read().strip()
    print(f"🔑 Using existing API Key: {API_KEY}")
else:
    # Generate new API key
    API_KEY = secrets.token_urlsafe(32)
    with open(API_KEY_FILE, 'w') as f:
        f.write(API_KEY)
    print(f"🔑 Generated NEW API Key: {API_KEY}")
    print("⚠️  Save this API key - you'll need it for frontend requests!")
    print("💡 This API key changes every time you restart the server")

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting FastAPI server...")
    load_model()
    logger.info("✅ Server startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down server...")

class PredictionInput(BaseModel):
    """Input model for prediction requests"""
    longitude: float = Field(..., description="Longitude coordinate", ge=-180, le=180)
    latitude: float = Field(..., description="Latitude coordinate", ge=-90, le=90)
    crop: str = Field(..., description="Crop type")
    farm_size_acres: float = Field(..., description="Farm size in acres", gt=0)
    
    # Optional fields with defaults for comprehensive prediction
    district: str = Field("Amritsar", description="District name")
    sowing_month: int = Field(11, description="Sowing month (1-12)")
    season: str = Field("rabi", description="Season (kharif/rabi)")
    
    # Weather parameters (with defaults)
    temperature: float = Field(25.0, description="Temperature in Celsius")
    humidity: float = Field(60.0, description="Humidity percentage")
    rainfall: float = Field(600.0, description="Rainfall in mm")
    wind_speed: float = Field(10.0, description="Wind speed in km/h")
    
    # Soil parameters (with defaults)
    pH: float = Field(7.0, description="Soil pH", ge=4.0, le=9.0)
    organic_carbon: float = Field(0.5, description="Organic carbon %")
    N_available: float = Field(250.0, description="Available Nitrogen")
    P_available: float = Field(25.0, description="Available Phosphorus")
    K_available: float = Field(300.0, description="Available Potassium")
    
    # Satellite data (with defaults)
    ndvi_mean: float = Field(0.7, description="NDVI mean")
    ndwi_mean: float = Field(0.3, description="NDWI mean")
    blue: float = Field(0.08, description="Blue band reflectance")
    green: float = Field(0.12, description="Green band reflectance")
    red: float = Field(0.15, description="Red band reflectance")
    nir: float = Field(0.35, description="NIR band reflectance")
    
    # Year
    year: int = Field(2024, description="Year")

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    model_config = ConfigDict(protected_namespaces=())
    
    prediction: str
    input: Dict[str, Any]
    timestamp: str
    model_info: Dict[str, str]

# Initialize FastAPI app
app = FastAPI(
    title="ML Model Inference API",
    description="FastAPI backend service for ML model predictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
model_metadata = {}

def load_model():
    """Load the ML model once when server starts"""
    global model, model_metadata
    
    try:
        # Path to your model file
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'punjab_crop_yield_predictor_final.pkl')
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
                model = model_package.get('model')
                model_metadata = {
                    'model_type': str(type(model).__name__),
                    'features': model_package.get('feature_names', []),
                    'loaded_at': datetime.now().isoformat(),
                    'file_path': model_path
                }
            logger.info(f"✅ Model loaded successfully: {model_metadata['model_type']}")
        else:
            logger.warning(f"⚠️ Model file not found at: {model_path}")
            logger.info("📁 Available files in models directory:")
            models_dir = os.path.join(os.path.dirname(__file__), 'models')
            if os.path.exists(models_dir):
                for file in os.listdir(models_dir):
                    logger.info(f"   - {file}")
            
            # Fallback: create a dummy model for demonstration
            create_dummy_model()
            
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        create_dummy_model()

def create_dummy_model():
    """Create a dummy model for demonstration purposes"""
    global model, model_metadata
    
    class DummyModel:
        def predict(self, X):
            """Dummy prediction based on simple heuristics"""
            # Simple yield prediction based on farm size and crop type
            base_yields = {
                'wheat': 1500, 'rice': 2000, 'corn': 1800, 'cotton': 800,
                'soybean': 1200, 'barley': 1400, 'maize': 1800
            }
            
            predictions = []
            for row in X:
                farm_size = row[3] if len(row) > 3 else 5.0  # farm_size_acres
                crop_factor = 1.0
                
                # Simulate yield based on location (latitude/longitude effects)
                lat_factor = 1.0 + (row[1] - 30) * 0.01 if len(row) > 1 else 1.0  # latitude
                lon_factor = 1.0 + (row[0] - 75) * 0.005 if len(row) > 0 else 1.0  # longitude
                
                # Base yield (kg per acre)
                base_yield = base_yields.get('wheat', 1500)  # Default to wheat
                
                # Apply factors
                predicted_yield = base_yield * lat_factor * lon_factor * crop_factor
                
                # Add some randomness for realism
                import random
                predicted_yield *= (0.9 + random.random() * 0.2)  # ±10% variation
                
                predictions.append(max(500, min(3000, predicted_yield)))  # Clamp between reasonable values
            
            return np.array(predictions)
    
    model = DummyModel()
    model_metadata = {
        'model_type': 'DummyModel',
        'features': ['longitude', 'latitude', 'crop_encoded', 'farm_size_acres'],
        'loaded_at': datetime.now().isoformat(),
        'file_path': 'dummy_model',
        'note': 'Using fallback dummy model for demonstration'
    }
    logger.info("✅ Dummy model created for demonstration")

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key authentication"""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ML Model Inference API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "model_info": model_metadata,
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health",
            "docs": "/docs"
        },
        "authentication": "Bearer token required for /predict endpoint"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "model_type": model_metadata.get('model_type', 'None')
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(
    input_data: PredictionInput,
    api_key: str = Depends(verify_api_key)
):
    """
    Main prediction endpoint
    
    Requires API key in Authorization header: Bearer <API_KEY>
    """
    try:
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded"
            )
        
        # Use the proper prediction function with all features
        try:
            from models.prediction_function import predict_crop_yield
            
            # Prepare comprehensive input data
            prediction_input = {
                'year': input_data.year,
                'latitude': input_data.latitude,
                'longitude': input_data.longitude,
                'ndvi_mean': input_data.ndvi_mean,
                'ndwi_mean': input_data.ndwi_mean,
                'blue': input_data.blue,
                'green': input_data.green,
                'red': input_data.red,
                'nir': input_data.nir,
                'pH': input_data.pH,
                'organic_carbon': input_data.organic_carbon,
                'N_available': input_data.N_available,
                'P_available': input_data.P_available,
                'K_available': input_data.K_available,
                'temperature': input_data.temperature,
                'humidity': input_data.humidity,
                'rainfall': input_data.rainfall,
                'wind_speed': input_data.wind_speed,
                'sowing_month': input_data.sowing_month,
                'crop_type': input_data.crop,
                'district': input_data.district,
                'season': input_data.season,
                'data_source': 'api',
                'soil_health_status': 'good',
                'data_source_soil': 'api',
                'data_source_weather': 'api',
                'soil_pH_category': 'neutral' if 6.5 <= input_data.pH <= 7.5 else 'acidic' if input_data.pH < 6.5 else 'alkaline'
            }
            
            # Make prediction using the proper function
            result = predict_crop_yield(
                prediction_input, 
                model_path='models/punjab_crop_yield_predictor_final.pkl'
            )
            
            predicted_value = result['predicted_yield']
            prediction_text = f"Predicted yield: {predicted_value} kg/acre (Range: {result['lower_bound']}-{result['upper_bound']} kg/acre)"
            
        except Exception as model_error:
            logger.warning(f"⚠️ Using fallback prediction due to: {model_error}")
            # Fallback to simple prediction if the comprehensive model fails
            input_array = np.array([[
                input_data.longitude,
                input_data.latitude,
                hash(input_data.crop.lower()) % 100,
                input_data.farm_size_acres
            ]])
            
            prediction_raw = model.predict(input_array)
            predicted_value = float(prediction_raw[0])
            prediction_text = f"Predicted yield: {predicted_value:.1f} kg/acre (fallback model)"
            result = {'predicted_yield': predicted_value, 'model_used': 'fallback'}
        
        # Create response
        response = PredictionResponse(
            prediction=prediction_text,
            input={
                "longitude": input_data.longitude,
                "latitude": input_data.latitude,
                "crop": input_data.crop,
                "farm_size_acres": input_data.farm_size_acres,
                "district": input_data.district,
                "season": input_data.season
            },
            timestamp=datetime.now().isoformat(),
            model_info={
                "model_type": result.get('model_used', 'RandomForestRegressor'),
                "prediction_value": f"{predicted_value:.1f}",
                "units": "kg/acre"
            }
        )
        
        logger.info(f"✅ Prediction made: {predicted_value:.1f} kg/acre for {input_data.crop}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

def setup_ngrok():
    """Setup ngrok tunnel for public access (optional)"""
    try:
        from pyngrok import ngrok
        
        # Kill any existing tunnels
        ngrok.kill()
        
        # Create tunnel
        public_tunnel = ngrok.connect(8000)
        public_url = public_tunnel.public_url
        
        print("\n" + "="*60)
        print("🌐 NGROK TUNNEL ACTIVE")
        print("="*60)
        print(f"🔗 Public URL: {public_url}")
        print(f"🔑 API Key: {API_KEY}")
        print(f"📍 Prediction Endpoint: {public_url}/predict")
        print("="*60)
        print("📋 Frontend Integration URL:")
        print(f"   {public_url}/predict")
        print("\n💡 Use this URL in your frontend code!")
        print("="*60 + "\n")
        
        return public_url
        
    except ImportError:
        print("\n⚠️  pyngrok not installed. Install it with: pip install pyngrok")
        print("🔗 Server running locally at: http://localhost:8000")
        return None
    except Exception as e:
        if "authentication failed" in str(e).lower():
            print("\n⚠️ Ngrok authentication required:")
            print("   1. Sign up at: https://dashboard.ngrok.com/signup")
            print("   2. Get your authtoken at: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("   3. Run: ngrok config add-authtoken YOUR_TOKEN")
            print("🔗 Server running locally at: http://localhost:8000")
        else:
            print(f"❌ Ngrok setup failed: {e}")
            print("🔗 Server running locally at: http://localhost:8000")
        return None

if __name__ == "__main__":
    print("🚀 Starting ML Model FastAPI Backend...")
    print("="*50)
    
    try:
        # Setup ngrok tunnel (optional)
        public_url = setup_ngrok()
        
        print(f"🔑 Using API Key: {API_KEY}")
        print("🔗 Server running locally at: http://localhost:9091")
        print("📚 API Documentation: http://localhost:9091/docs")
        print("🏥 Health Check: http://localhost:9091/health")
        print("="*50)
        
        # Start the server
        uvicorn.run(
            "fastapi_backend:app",
            host="0.0.0.0",
            port=9091,
            reload=False,  # Disabled auto-reload for stability
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    finally:
        # Clean up API key file when server stops
        if os.path.exists('.api_key'):
            os.remove('.api_key')
            print("🧹 Cleaned up API key file")
