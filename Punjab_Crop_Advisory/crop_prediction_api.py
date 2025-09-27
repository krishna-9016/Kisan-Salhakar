"""
Crop Prediction API Service
==========================

Standalone API service for crop yield prediction with API key authentication.
This service is designed to be integrated into larger UI projects.

Features:
- API key authentication
- Simple JSON input/output
- Smart parameter estimation
- Production-ready error handling
- CORS enabled for frontend integration
"""

import os
import secrets
import pickle
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration - Single API Key
SINGLE_API_KEY = "punjab_crop_api_2024"

# Security
security = HTTPBearer()

class CropPredictionRequest(BaseModel):
    """Simplified input model - only 4 essential fields"""
    crop: str = Field(..., description="Crop type (wheat, rice, corn, etc.)")
    acres: float = Field(..., description="Farm size in acres", gt=0)
    latitude: float = Field(..., description="Farm latitude", ge=29.0, le=33.0)
    longitude: float = Field(..., description="Farm longitude", ge=73.0, le=77.0)
    
    # Optional parameters for advanced users
    year: Optional[int] = Field(None, description="Year (defaults to current year)")
    season: Optional[str] = Field(None, description="Season (auto-detected if not provided)")

class CropRecommendation(BaseModel):
    """Crop recommendation model"""
    crop_name: str
    suitability_score: float
    expected_yield: float
    profitability: str
    reasons: list[str]
    tips: list[str]

class CropPredictionResponse(BaseModel):
    """API response model"""
    model_config = ConfigDict(protected_namespaces=())
    
    success: bool
    predicted_yield: float
    yield_range: Dict[str, float]
    confidence: str
    user_input: Dict[str, Any]
    estimated_parameters: Dict[str, Any]
    model_info: Dict[str, str]
    api_version: str
    timestamp: str
    
    # New fields for recommendations
    crop_recommendations: list[CropRecommendation]
    farming_tips: list[str]
    seasonal_advice: str

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    error_code: str
    timestamp: str

# Initialize FastAPI app
app = FastAPI(
    title="Punjab Crop Prediction API",
    description="AI-powered crop yield prediction API for Punjab agriculture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific domains in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Global variables
model = None
model_metadata = {}

def load_prediction_model():
    """Load the ML model"""
    global model, model_metadata
    
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'punjab_crop_yield_predictor_final.pkl')
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
                model = model_package.get('model')
                model_metadata = {
                    'model_type': str(type(model).__name__),
                    'loaded_at': datetime.now().isoformat(),
                    'version': '1.0.0'
                }
            logger.info(f"✅ Model loaded: {model_metadata['model_type']}")
        else:
            # Create dummy model for demonstration
            model = create_dummy_model()
            model_metadata = {
                'model_type': 'DummyModel',
                'loaded_at': datetime.now().isoformat(),
                'version': '1.0.0-demo'
            }
            logger.warning("⚠️ Using demo model - production model not found")
            
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        model = create_dummy_model()
        model_metadata = {
            'model_type': 'DummyModel',
            'loaded_at': datetime.now().isoformat(),
            'version': '1.0.0-fallback'
        }

def create_dummy_model():
    """Create demo model for testing"""
    class DummyModel:
        def predict(self, X):
            predictions = []
            for row in X:
                # Smart prediction based on crop type and location
                base_yields = {
                    'wheat': 1800, 'rice': 2200, 'corn': 2000, 'maize': 2000,
                    'cotton': 900, 'soybean': 1300, 'barley': 1600, 'mustard': 1100
                }
                
                crop_hash = hash(str(row[2]).lower()) % len(base_yields)
                crop_types = list(base_yields.keys())
                estimated_crop = crop_types[crop_hash % len(crop_types)]
                
                base_yield = base_yields.get(estimated_crop, 1500)
                
                # Location and size factors
                lat_factor = 1.0 + (row[1] - 31.0) * 0.02  # latitude effect
                size_factor = min(1.2, 1.0 + (row[0] - 5.0) * 0.01)  # farm size effect
                
                predicted_yield = base_yield * lat_factor * size_factor
                
                # Add realistic variation
                import random
                variation = 0.85 + random.random() * 0.3  # ±15% variation
                predicted_yield *= variation
                
                predictions.append(max(800, min(3500, predicted_yield)))
            
            return np.array(predictions)
    
    return DummyModel()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key authentication"""
    token = credentials.credentials
    
    if token != SINGLE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

def get_crop_recommendations(latitude: float, longitude: float, current_crop: str, farm_size: float, season: str) -> list[CropRecommendation]:
    """Generate intelligent crop recommendations based on location and conditions"""
    
    # Punjab crop database with suitability factors
    crop_database = {
        'wheat': {
            'base_yield': 1800,
            'seasons': ['rabi'],
            'min_temp': 15, 'max_temp': 25,
            'water_requirement': 'medium',
            'soil_ph': [6.5, 7.5],
            'profitability': 'High',
            'market_demand': 'Very High'
        },
        'rice': {
            'base_yield': 2200,
            'seasons': ['kharif'],
            'min_temp': 22, 'max_temp': 35,
            'water_requirement': 'high',
            'soil_ph': [6.0, 7.0],
            'profitability': 'High',
            'market_demand': 'Very High'
        },
        'cotton': {
            'base_yield': 900,
            'seasons': ['kharif'],
            'min_temp': 20, 'max_temp': 35,
            'water_requirement': 'medium',
            'soil_ph': [5.8, 8.0],
            'profitability': 'Very High',
            'market_demand': 'High'
        },
        'maize': {
            'base_yield': 2000,
            'seasons': ['kharif', 'rabi'],
            'min_temp': 18, 'max_temp': 32,
            'water_requirement': 'medium',
            'soil_ph': [6.0, 7.5],
            'profitability': 'Medium',
            'market_demand': 'High'
        },
        'sugarcane': {
            'base_yield': 2800,
            'seasons': ['annual'],
            'min_temp': 20, 'max_temp': 35,
            'water_requirement': 'very_high',
            'soil_ph': [6.5, 7.5],
            'profitability': 'Very High',
            'market_demand': 'High'
        },
        'mustard': {
            'base_yield': 1100,
            'seasons': ['rabi'],
            'min_temp': 10, 'max_temp': 25,
            'water_requirement': 'low',
            'soil_ph': [6.0, 7.5],
            'profitability': 'Medium',
            'market_demand': 'Medium'
        },
        'barley': {
            'base_yield': 1600,
            'seasons': ['rabi'],
            'min_temp': 12, 'max_temp': 22,
            'water_requirement': 'low',
            'soil_ph': [6.0, 7.8],
            'profitability': 'Medium',
            'market_demand': 'Medium'
        },
        'potato': {
            'base_yield': 2500,
            'seasons': ['rabi'],
            'min_temp': 15, 'max_temp': 25,
            'water_requirement': 'medium',
            'soil_ph': [5.5, 6.5],
            'profitability': 'High',
            'market_demand': 'Very High'
        }
    }
    
    recommendations = []
    current_season = season.lower()
    
    # Calculate location factors
    lat_factor = 1.0 + (latitude - 31.0) * 0.02  # Punjab latitude effect
    size_factor = min(1.2, 1.0 + (farm_size - 5.0) * 0.01)  # Farm size effect
    
    for crop_name, crop_data in crop_database.items():
        if crop_name.lower() == current_crop.lower():
            continue  # Skip current crop
            
        # Check season compatibility
        if current_season not in crop_data['seasons'] and 'annual' not in crop_data['seasons']:
            continue
            
        # Calculate suitability score
        suitability_score = 0.7  # Base score
        
        # Location bonus (central Punjab is better)
        if 30.5 <= latitude <= 31.5 and 75.0 <= longitude <= 76.5:
            suitability_score += 0.2
        
        # Farm size bonus
        if farm_size >= 10:
            suitability_score += 0.1
        
        # Calculate expected yield
        expected_yield = crop_data['base_yield'] * lat_factor * size_factor
        
        # Generate reasons for recommendation
        reasons = []
        if crop_data['profitability'] in ['High', 'Very High']:
            reasons.append(f"High profitability - {crop_data['profitability']} returns expected")
        if crop_data['market_demand'] in ['High', 'Very High']:
            reasons.append(f"Strong market demand - {crop_data['market_demand']} buyer interest")
        if crop_data['water_requirement'] == 'low':
            reasons.append("Water efficient - suitable for sustainable farming")
        if latitude > 31.0 and crop_name in ['wheat', 'rice']:
            reasons.append("Excellent climate match for this region")
        if farm_size >= 20 and crop_name in ['cotton', 'sugarcane']:
            reasons.append("Large farm size ideal for commercial cultivation")
        
        # Generate crop-specific tips
        tips = get_crop_specific_tips(crop_name, latitude, longitude, farm_size)
        
        recommendations.append(CropRecommendation(
            crop_name=crop_name.title(),
            suitability_score=round(min(1.0, suitability_score), 2),
            expected_yield=round(expected_yield, 1),
            profitability=crop_data['profitability'],
            reasons=reasons[:3],  # Top 3 reasons
            tips=tips[:3]  # Top 3 tips
        ))
    
    # Sort by suitability score and expected yield
    recommendations.sort(key=lambda x: (x.suitability_score, x.expected_yield), reverse=True)
    
    return recommendations[:5]  # Top 5 recommendations

def get_crop_specific_tips(crop_name: str, latitude: float, longitude: float, farm_size: float) -> list[str]:
    """Generate crop-specific farming tips"""
    
    tips_database = {
        'wheat': [
            "Plant wheat in November for optimal yield in Punjab climate",
            "Use certified seeds with 100-120 kg/acre seeding rate",
            "Apply balanced NPK fertilizer: 120:60:30 kg/acre",
            "Ensure 4-5 irrigations during growing season",
            "Monitor for rust diseases and apply fungicides if needed",
            "Harvest when moisture content is 20-25% for best quality"
        ],
        'rice': [
            "Transplant 25-30 day old seedlings in June-July",
            "Maintain 2-3 cm water level throughout growing season",
            "Use recommended varieties like PR-126, PR-121 for Punjab",
            "Apply silicon fertilizer to strengthen stems",
            "Practice direct seeded rice (DSR) to save water",
            "Monitor for brown plant hopper and stem borer"
        ],
        'cotton': [
            "Plant Bt cotton varieties approved for Punjab",
            "Sow in May for optimal fiber quality",
            "Maintain plant population of 80,000-100,000 plants/acre",
            "Deep plowing and good drainage essential",
            "Regular monitoring for pink bollworm required",
            "Harvest when 60% bolls are open for best fiber quality"
        ],
        'maize': [
            "Use hybrid varieties for higher yield potential",
            "Plant with 60cm row spacing and 20cm plant distance",
            "Side-dress nitrogen at knee-high stage",
            "Ensure adequate moisture during tasseling and grain filling",
            "Monitor for fall armyworm and stem borer",
            "Harvest at 18-20% moisture for good storage"
        ],
        'sugarcane': [
            "Plant healthy setts from 8-10 month old canes",
            "Ensure proper drainage to prevent water logging",
            "Apply organic manure before planting",
            "Regular earthing up and gap filling essential",
            "Monitor for red rot and smut diseases",
            "Harvest at optimal maturity (12 months) for maximum sugar"
        ],
        'mustard': [
            "Sow in October for timely harvest before heat",
            "Use line sowing with 30cm row spacing",
            "Light irrigation during flowering stage",
            "Apply sulfur fertilizer for better oil content",
            "Monitor for aphids and white rust disease",
            "Harvest when pods turn brown but not fully dry"
        ],
        'barley': [
            "Choose malting or feed varieties based on market",
            "Sow in November for avoiding heat stress",
            "Requires less water compared to wheat",
            "Apply moderate nitrogen to avoid lodging",
            "Good rotation crop after paddy",
            "Harvest when grain moisture is around 20%"
        ],
        'potato': [
            "Use certified seed potatoes for disease-free crop",
            "Plant in raised beds for better drainage",
            "Hill up regularly to prevent greening of tubers",
            "Monitor soil moisture - avoid over and under watering",
            "Watch for late blight especially in humid conditions",
            "Harvest when skin is firm and doesn't rub off easily"
        ]
    }
    
    crop_tips = tips_database.get(crop_name.lower(), [
        f"Research best practices for {crop_name} cultivation",
        f"Consult local agricultural extension officer for {crop_name} guidance",
        f"Consider market prices before growing {crop_name}"
    ])
    
    # Add location-specific tips
    location_tips = []
    if latitude > 31.5:
        location_tips.append("Your northern location is ideal for cool-season crops")
    elif latitude < 30.5:
        location_tips.append("Your southern location suits warm-season crops better")
    
    if farm_size >= 50:
        location_tips.append("Consider mechanization for large farm operations")
    elif farm_size <= 5:
        location_tips.append("Focus on intensive cultivation methods for small farms")
    
    return crop_tips + location_tips

def get_general_farming_tips(season: str, latitude: float, farm_size: float) -> list[str]:
    """Generate general farming tips based on season and location"""
    
    tips = [
        "Conduct soil testing every 2-3 years for optimal fertilizer management",
        "Practice crop rotation to maintain soil health and break pest cycles",
        "Use drip irrigation or sprinkler systems to conserve water",
        "Maintain farm records for input costs and yield tracking",
        "Join farmer producer organizations (FPOs) for better market access"
    ]
    
    # Season-specific tips
    if season.lower() == 'kharif':
        tips.extend([
            "Ensure proper drainage during monsoon season",
            "Monitor weather forecasts for pest and disease outbreaks",
            "Stock up on plant protection chemicals before monsoon"
        ])
    elif season.lower() == 'rabi':
        tips.extend([
            "Plan irrigation schedule as winter has less rainfall",
            "Take advantage of cooler weather for farm operations",
            "Prepare for harvesting equipment rental in advance"
        ])
    
    # Location-specific tips
    if latitude > 31.0:
        tips.append("Take advantage of your region's reputation for quality wheat")
    
    # Farm size specific tips
    if farm_size >= 25:
        tips.append("Consider contract farming for assured market and prices")
    else:
        tips.append("Focus on value addition and direct marketing")
    
    return tips[:6]  # Return top 6 tips

def get_seasonal_advice(season: str, latitude: float, current_month: int = None) -> str:
    """Generate seasonal farming advice"""
    
    if current_month is None:
        current_month = datetime.now().month
    
    advice = ""
    
    if season.lower() == 'rabi':
        if current_month in [10, 11]:
            advice = "🌾 RABI SEASON: Perfect time for wheat sowing. Prepare fields and arrange quality seeds. " \
                    "Ensure timely planting to avoid heat stress during grain filling stage."
        elif current_month in [12, 1, 2]:
            advice = "❄️ WINTER CARE: Monitor crop growth and provide irrigation as needed. " \
                    "Watch for pest infestations in cool weather. Apply nitrogen top-dressing if required."
        elif current_month in [3, 4]:
            advice = "🌾 HARVEST TIME: Prepare for rabi harvest. Check grain moisture and arrange harvest machinery. " \
                    "Plan for immediate marketing or proper storage to avoid post-harvest losses."
        else:
            advice = "🔄 FIELD PREPARATION: Use this time for land preparation, soil testing, and planning next rabi season. " \
                    "Consider green manuring with summer crops."
    
    elif season.lower() == 'kharif':
        if current_month in [5, 6]:
            advice = "🌱 KHARIF PREPARATION: Prepare nurseries for rice and get ready for kharif sowing. " \
                    "Ensure water availability and check irrigation systems. Pre-monsoon field preparation is crucial."
        elif current_month in [7, 8, 9]:
            advice = "🌧️ MONSOON SEASON: Monitor crops for pest and disease outbreaks. Ensure proper drainage. " \
                    "This is crucial growth period - maintain optimal plant nutrition and protection."
        elif current_month in [10, 11]:
            advice = "🌾 KHARIF HARVEST: Prepare for kharif harvest. Monitor grain maturity and weather forecasts. " \
                    "Plan storage facilities and explore marketing options for better prices."
        else:
            advice = "☀️ SUMMER SEASON: Consider summer crops like fodder maize or green manure crops. " \
                    "This is ideal time for deep plowing and soil health improvement activities."
    
    # Add location-specific advice
    if latitude > 31.5:
        advice += " Your northern Punjab location has advantages for wheat cultivation and cooler climate crops."
    elif latitude < 30.5:
        advice += " Your location is well-suited for cotton and other warm-season crops."
    
    return advice

def estimate_parameters(crop: str, district: str, latitude: float, longitude: float, year: int = None) -> Dict[str, Any]:
    """Estimate weather and soil parameters based on location and crop"""
    
    if year is None:
        year = datetime.now().year
    
    # Season detection based on crop type
    rabi_crops = ['wheat', 'barley', 'mustard', 'potato', 'peas']
    kharif_crops = ['rice', 'corn', 'maize', 'cotton', 'soybean', 'sugarcane']
    
    if crop.lower() in rabi_crops:
        season = 'rabi'
        sowing_month = 11
    elif crop.lower() in kharif_crops:
        season = 'kharif'
        sowing_month = 6
    else:
        season = 'rabi'  # default
        sowing_month = 11
    
    # Location-based parameter estimation
    lat_factor = (latitude - 31.0) * 0.4
    lon_factor = (longitude - 75.5) * 0.3
    
    # Weather parameters with Punjab regional variations
    if season == 'rabi':
        temperature = 22.0 + lat_factor
        humidity = 70.0 - abs(lat_factor) * 2
        rainfall = 550.0 + lat_factor * 25
    else:  # kharif
        temperature = 28.0 + lat_factor
        humidity = 75.0 - abs(lat_factor)
        rainfall = 800.0 + lat_factor * 40
    
    wind_speed = 8.0 + abs(lon_factor)
    
    # Soil parameters (Punjab typical values)
    pH = 7.1 + (latitude - 31.0) * 0.1  # slight pH variation
    organic_carbon = 0.6 + lon_factor * 0.05
    N_available = 270.0 + lat_factor * 10
    P_available = 22.0 + lon_factor * 2
    K_available = 310.0 + lat_factor * 15
    
    # Satellite data (healthy crop assumptions)
    ndvi_mean = 0.75
    ndwi_mean = 0.35
    blue = 0.08
    green = 0.12
    red = 0.15
    nir = 0.40
    
    return {
        'year': year,
        'latitude': latitude,
        'longitude': longitude,
        'season': season,
        'sowing_month': sowing_month,
        'temperature': round(temperature, 1),
        'humidity': round(humidity, 1),
        'rainfall': round(rainfall, 0),
        'wind_speed': round(wind_speed, 1),
        'pH': round(pH, 1),
        'organic_carbon': round(organic_carbon, 2),
        'N_available': round(N_available, 1),
        'P_available': round(P_available, 1),
        'K_available': round(K_available, 1),
        'ndvi_mean': ndvi_mean,
        'ndwi_mean': ndwi_mean,
        'blue': blue,
        'green': green,
        'red': red,
        'nir': nir
    }

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("🚀 Starting Crop Prediction API...")
    load_prediction_model()
    logger.info("✅ API ready for requests")

@app.get("/")
async def root():
    """API information"""
    return {
        "service": "Punjab Crop Prediction API",
        "version": "1.0.0",
        "status": "active",
        "model_loaded": model is not None,
        "authentication": "Bearer token required",
        "endpoints": {
            "predict": "POST /api/v1/predict",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "usage": "Include 'Authorization: Bearer YOUR_API_KEY' header"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": model_metadata.get('model_type', 'None'),
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }

@app.post("/api/v1/predict", response_model=CropPredictionResponse)
async def predict_crop_yield(
    request: CropPredictionRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Predict crop yield based on essential farm parameters
    
    Requires API key in Authorization header: Bearer YOUR_API_KEY
    """
    try:
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Prediction model not available"
            )
        
        # Estimate all parameters based on user input
        # For simplified input, we'll use default district and year
        estimated_params = estimate_parameters(
            crop=request.crop,
            district="Ludhiana",  # Default district
            latitude=request.latitude,
            longitude=request.longitude,
            year=2025
        )
        
        # Prepare features for model prediction using all estimated parameters
        # The model expects 39 features, so we'll use all estimated parameters
        
        # Create feature array with all estimated parameters
        features = np.array([[
            request.acres,                          # farm_size_acres
            request.latitude,                       # latitude
            request.longitude,                      # longitude
            estimated_params['temperature'],        # temperature
            estimated_params['humidity'],           # humidity
            estimated_params['rainfall'],           # rainfall
            estimated_params['wind_speed'],         # wind_speed
            estimated_params['pH'],                 # pH
            estimated_params['organic_carbon'],     # organic_carbon
            estimated_params['N_available'],        # N_available
            estimated_params['P_available'],        # P_available
            estimated_params['K_available'],        # K_available
            estimated_params['ndvi_mean'],          # ndvi_mean
            estimated_params['ndwi_mean'],          # ndwi_mean
            estimated_params['blue'],               # blue
            estimated_params['green'],              # green
            estimated_params['red'],                # red
            estimated_params['nir'],                # nir
            hash(request.crop.lower()) % 100,       # crop_encoded
            1 if estimated_params['season'] == 'Kharif' else 0,    # season_Kharif
            1 if estimated_params['season'] == 'Rabi' else 0,      # season_Rabi
            1 if estimated_params['season'] == 'Summer' else 0,    # season_Summer
            1 if estimated_params['sowing_month'] == 1 else 0,     # month_1
            1 if estimated_params['sowing_month'] == 2 else 0,     # month_2
            1 if estimated_params['sowing_month'] == 3 else 0,     # month_3
            1 if estimated_params['sowing_month'] == 4 else 0,     # month_4
            1 if estimated_params['sowing_month'] == 5 else 0,     # month_5
            1 if estimated_params['sowing_month'] == 6 else 0,     # month_6
            1 if estimated_params['sowing_month'] == 7 else 0,     # month_7
            1 if estimated_params['sowing_month'] == 8 else 0,     # month_8
            1 if estimated_params['sowing_month'] == 9 else 0,     # month_9
            1 if estimated_params['sowing_month'] == 10 else 0,    # month_10
            1 if estimated_params['sowing_month'] == 11 else 0,    # month_11
            1 if estimated_params['sowing_month'] == 12 else 0,    # month_12
            2025,                                   # year
            1,                                      # district_encoded (default)
            30.0,                                   # elevation (default)
            0.8,                                    # irrigation_efficiency (default)
            1.0                                     # fertilizer_efficiency (default)
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Calculate confidence intervals (±15% for demo)
        lower_bound = prediction * 0.85
        upper_bound = prediction * 1.15
        
        # Determine confidence level
        if prediction > 2000:
            confidence = "High"
        elif prediction > 1200:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Generate crop recommendations and farming tips
        crop_recommendations = get_crop_recommendations(
            latitude=request.latitude,
            longitude=request.longitude,
            current_crop=request.crop,
            farm_size=request.acres,
            season=estimated_params['season']
        )
        
        farming_tips = get_general_farming_tips(
            season=estimated_params['season'],
            latitude=request.latitude,
            farm_size=request.acres
        )
        
        seasonal_advice = get_seasonal_advice(
            season=estimated_params['season'],
            latitude=request.latitude
        )
        
        # Build response
        response = CropPredictionResponse(
            success=True,
            predicted_yield=round(prediction, 1),
            yield_range={
                "minimum": round(lower_bound, 1),
                "maximum": round(upper_bound, 1)
            },
            confidence=confidence,
            user_input={
                "crop": request.crop,
                "district": "Ludhiana",  # Default district
                "farm_size_acres": request.acres,
                "latitude": request.latitude,
                "longitude": request.longitude
            },
            estimated_parameters={
                "season": estimated_params['season'],
                "temperature": f"{estimated_params['temperature']}°C",
                "humidity": f"{estimated_params['humidity']}%",
                "rainfall": f"{estimated_params['rainfall']}mm",
                "soil_pH": estimated_params['pH']
            },
            model_info={
                "model_type": model_metadata.get('model_type', 'Unknown'),
                "version": model_metadata.get('version', '1.0.0'),
                "units": "kg/acre"
            },
            api_version="1.0.0",
            timestamp=datetime.now().isoformat(),
            crop_recommendations=crop_recommendations,
            farming_tips=farming_tips,
            seasonal_advice=seasonal_advice
        )
        
        logger.info(f"✅ Prediction: {prediction:.1f} kg/acre for {request.crop} in Ludhiana")
        return response
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/api/v1/crops")
async def get_supported_crops(api_key: str = Depends(verify_api_key)):
    """Get list of supported crops"""
    return {
        "crops": [
            "wheat", "rice", "corn", "maize", "cotton", "soybean", 
            "barley", "mustard", "potato", "sugarcane", "tomato", "onion"
        ],
        "rabi_crops": ["wheat", "barley", "mustard", "potato", "peas"],
        "kharif_crops": ["rice", "corn", "maize", "cotton", "soybean", "sugarcane"]
    }

@app.get("/api/v1/districts")
async def get_supported_districts(api_key: str = Depends(verify_api_key)):
    """Get list of Punjab districts"""
    return {
        "districts": [
            "Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda",
            "Mohali", "Gurdaspur", "Kapurthala", "Hoshiarpur", "Faridkot",
            "Firozpur", "Muktsar", "Sangrur", "Barnala", "Mansa",
            "Nawanshahr", "Ropar", "Fatehgarh Sahib", "Moga", "Pathankot",
            "Fazilka", "Tarn Taran"
        ]
    }

if __name__ == "__main__":
    print("\n🌾 Punjab Crop Prediction API Service")
    print("=" * 45)
    print(f"🔑 API Key: {SINGLE_API_KEY}")
    print("\n🔗 API Endpoints:")
    print("   • POST /api/v1/predict  - Crop yield prediction")
    print("   • GET  /api/v1/crops    - Supported crops")
    print("   • GET  /api/v1/districts - Punjab districts")
    print("   • GET  /health          - Health check")
    print("   • GET  /docs            - API documentation")
    print("\n📖 Usage:")
    print("   Authorization: Bearer YOUR_API_KEY")
    print("=" * 45)
    print("\n🚀 Starting API server...")
    
    uvicorn.run(
        "crop_prediction_api:app",
        host="0.0.0.0",
        port=9090,
        reload=False,
        log_level="info"
    )
