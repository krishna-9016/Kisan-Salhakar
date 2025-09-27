"""
Flask Frontend Application for Crop Prediction System
====================================================

This Flask app provides a web interface that integrates with the FastAPI backend
for crop yield predictions. It includes:
- User-friendly forms for input
- API integration with the FastAPI backend
- Results display with visualizations
- Responsive web design
"""

import os
import requests
import json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'crop_prediction_secret_key_2024'  # Change this in production

# FastAPI backend configuration
FASTAPI_BASE_URL = "http://localhost:9090"
FASTAPI_API_KEY = "AmCElo0bX6r6b2C0n9iLkInFKwEqYL72M75-ja1t1S0"  # Update this with your actual API key

# Default crop types available
CROP_TYPES = [
    'wheat', 'rice', 'corn', 'cotton', 'soybean', 'barley', 'maize',
    'sugarcane', 'potato', 'tomato', 'onion', 'mustard'
]

# Punjab districts
PUNJAB_DISTRICTS = [
    'Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala', 'Bathinda',
    'Mohali', 'Gurdaspur', 'Kapurthala', 'Hoshiarpur', 'Faridkot',
    'Firozpur', 'Muktsar', 'Sangrur', 'Barnala', 'Mansa',
    'Nawanshahr', 'Ropar', 'Fatehgarh Sahib', 'Moga', 'Pathankot',
    'Fazilka', 'Tarn Taran'
]

def check_fastapi_health():
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def make_prediction_request(prediction_data):
    """Make prediction request to FastAPI backend"""
    try:
        headers = {
            "Authorization": f"Bearer {FASTAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{FASTAPI_BASE_URL}/predict",
            json=prediction_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"API Error: {response.status_code} - {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to FastAPI backend. Please ensure it's running on localhost:8000"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout. The prediction is taking too long."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

@app.route('/')
def index():
    """Main page with prediction form"""
    backend_status = check_fastapi_health()
    return render_template('index.html', 
                         crop_types=CROP_TYPES, 
                         districts=PUNJAB_DISTRICTS,
                         backend_status=backend_status)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests with simplified input"""
    try:
        # Get form data
        form_data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Extract essential user inputs
        crop = form_data.get('crop', 'wheat')
        district = form_data.get('district', 'Amritsar')
        farm_size_acres = float(form_data.get('farm_size_acres', 5.0))
        latitude = float(form_data.get('latitude', 31.6340))
        longitude = float(form_data.get('longitude', 75.8573))
        
        # Smart defaults based on crop type and season
        current_month = datetime.now().month
        
        # Determine season and sowing month based on current time and crop
        if crop.lower() in ['wheat', 'barley', 'mustard', 'potato']:
            season = 'rabi'
            sowing_month = 11  # November for rabi crops
        else:
            season = 'kharif'
            sowing_month = 6   # June for kharif crops
        
        # Location-based weather defaults for Punjab
        # Adjust based on latitude (north-south variation)
        lat_factor = (latitude - 30.0) * 0.5  # Adjustment factor
        
        # Weather parameters with location-based adjustments
        temperature = 25.0 + lat_factor  # Slightly cooler in north Punjab
        humidity = 65.0 - lat_factor     # Slightly drier in north Punjab
        rainfall = 650.0 + lat_factor * 20  # More rainfall in north
        wind_speed = 8.0 + abs(lat_factor)  # Variable wind
        
        # Soil parameters - typical for Punjab agriculture
        pH = 7.2  # Slightly alkaline Punjab soils
        organic_carbon = 0.6  # Medium organic matter
        N_available = 280.0   # Good nitrogen availability
        P_available = 22.0    # Moderate phosphorus
        K_available = 320.0   # Good potassium
        
        # Satellite data defaults (typical NDVI for healthy crops)
        ndvi_mean = 0.75
        ndwi_mean = 0.35
        blue = 0.08
        green = 0.12
        red = 0.15
        nir = 0.40
        
        # Prepare comprehensive prediction data for FastAPI
        prediction_data = {
            "longitude": longitude,
            "latitude": latitude,
            "crop": crop,
            "farm_size_acres": farm_size_acres,
            "district": district,
            "sowing_month": sowing_month,
            "season": season,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "wind_speed": wind_speed,
            "pH": pH,
            "organic_carbon": organic_carbon,
            "N_available": N_available,
            "P_available": P_available,
            "K_available": K_available,
            "ndvi_mean": ndvi_mean,
            "ndwi_mean": ndwi_mean,
            "blue": blue,
            "green": green,
            "red": red,
            "nir": nir,
            "year": datetime.now().year
        }
        
        # Make prediction request
        result = make_prediction_request(prediction_data)
        
        if result["success"]:
            prediction_result = result["data"]
            return jsonify({
                "success": True,
                "prediction": prediction_result["prediction"],
                "input_data": {
                    "crop": crop,
                    "district": district,
                    "farm_size_acres": farm_size_acres,
                    "latitude": latitude,
                    "longitude": longitude,
                    "season": season,
                    "estimated_parameters": {
                        "temperature": f"{temperature:.1f}°C",
                        "humidity": f"{humidity:.1f}%",
                        "rainfall": f"{rainfall:.0f}mm",
                        "soil_pH": pH
                    }
                },
                "model_info": prediction_result["model_info"],
                "timestamp": prediction_result["timestamp"]
            })
        else:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
            
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Invalid input data: {str(e)}"
        }), 400
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal error: {str(e)}"
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    backend_status = check_fastapi_health()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "fastapi_backend": "connected" if backend_status else "disconnected"
    })

@app.route('/api-status')
def api_status():
    """Check FastAPI backend status"""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            return jsonify({
                "status": "connected",
                "backend_info": response.json()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Backend returned status {response.status_code}"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🌾 Starting Crop Prediction Flask Frontend...")
    print("="*50)
    print(f"🔗 Web Interface: http://localhost:5000")
    print(f"🤖 FastAPI Backend: {FASTAPI_BASE_URL}")
    print(f"🔑 API Key: {FASTAPI_API_KEY[:20]}...")
    print("="*50)
    
    # Check if backend is running
    if check_fastapi_health():
        print("✅ FastAPI backend is running")
    else:
        print("⚠️  FastAPI backend is not responding")
        print("   Please start it with: python fastapi_backend.py")
    
    print("\n🚀 Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=7070)
