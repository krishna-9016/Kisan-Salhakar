# Punjab Crop Advisory API - Frontend Integration Guide

## 🎯 Overview
This API provides crop yield predictions and farming recommendations for Punjab region based on coordinates, crop type, and farm size.

## 🚀 Quick Start

### 1. Start the API Server
```bash
# Windows
deploy_api.bat

# Linux/Mac  
bash deploy_api.sh

# Manual start
python api_deploy.py
```

### 2. API Base URL
```
http://localhost:5000/api
```

### 3. Health Check
```bash
curl http://localhost:5000/api/health
```

## 📡 API Endpoints

### GET /api/health
Check if the API is running
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00",
  "model_status": "loaded"
}
```

### GET /api/crops
Get list of supported crops
```json
{
  "crops": ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Bajra"],
  "count": 6
}
```

### POST /api/predict ⭐ **MAIN ENDPOINT**
Predict crop yield and get recommendations

**Request:**
```json
{
  "latitude": 30.9010,      // Required: 29.5-32.5 (Punjab region)
  "longitude": 75.8573,     // Required: 73.5-77.0 (Punjab region)
  "crop_name": "Wheat",     // Required: Must be from supported crops
  "farm_acres": 5.0         // Required: 0.1-10000 acres
}
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "request_info": {
    "latitude": 30.9010,
    "longitude": 75.8573,
    "crop_name": "Wheat",
    "farm_acres": 5.0,
    "location": "Ludhiana"
  },
  "prediction": {
    "yield_per_acre_kg": 1845.2,
    "total_production_kg": 9226.0,
    "confidence_interval": {
      "lower_kg": 1658.7,
      "upper_kg": 2031.7,
      "level": "95%"
    },
    "model_used": "ML_Model"
  },
  "economics": {
    "price_per_kg_inr": 25,
    "estimated_revenue_inr": 230650,
    "revenue_per_acre_inr": 46130
  },
  "environmental_data": {
    "weather": {
      "temperature": 25.3,
      "humidity": 68.2,
      "rainfall": 2.1,
      "wind_speed": 12.5,
      "weather_condition": "Clear"
    },
    "soil": {
      "pH": 7.2,
      "organic_carbon": 0.65,
      "nitrogen": 185.3,
      "phosphorus": 22.1,
      "potassium": 285.7,
      "soil_type": "Alluvial"
    },
    "satellite": {
      "ndvi_mean": 0.742,
      "ndwi_mean": 0.312,
      "acquisition_date": "2024-01-15",
      "cloud_cover": 12.5
    }
  },
  "recommendations": [
    {
      "type": "irrigation",
      "priority": "medium",
      "message": "Optimal irrigation schedule recommended",
      "icon": "💧"
    }
  ]
}
```

## 💻 Frontend Integration Examples

### JavaScript/React Example
```javascript
const predictCropYield = async (farmData) => {
  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: farmData.latitude,
        longitude: farmData.longitude,
        crop_name: farmData.cropName,
        farm_acres: farmData.farmSize
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    
    // Use the prediction data
    console.log('Predicted yield:', result.prediction.yield_per_acre_kg);
    console.log('Total production:', result.prediction.total_production_kg);
    console.log('Estimated revenue:', result.economics.estimated_revenue_inr);
    
    return result;
  } catch (error) {
    console.error('Prediction failed:', error);
    throw error;
  }
};

// Usage
const farmData = {
  latitude: 30.9010,
  longitude: 75.8573,
  cropName: 'Wheat',
  farmSize: 5.0
};

predictCropYield(farmData)
  .then(result => {
    // Handle successful prediction
    displayResults(result);
  })
  .catch(error => {
    // Handle error
    showErrorMessage(error.message);
  });
```

### Python Example (for testing)
```python
import requests
import json

def predict_crop_yield(latitude, longitude, crop_name, farm_acres):
    url = 'http://localhost:5000/api/predict'
    
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'crop_name': crop_name,
        'farm_acres': farm_acres
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Example usage
result = predict_crop_yield(30.9010, 75.8573, 'Wheat', 5.0)
print(json.dumps(result, indent=2))
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 30.9010,
    "longitude": 75.8573,
    "crop_name": "Wheat", 
    "farm_acres": 5.0
  }'
```

## 🛡️ Error Handling

### Validation Errors (400)
```json
{
  "error": "Missing required fields",
  "missing_fields": ["latitude"],
  "required_fields": ["latitude", "longitude", "crop_name", "farm_acres"]
}
```

### Coordinate Validation Error
```json
{
  "error": "Coordinates outside Punjab region",
  "valid_range": "Latitude: 29.5-32.5, Longitude: 73.5-77.0"
}
```

### Unsupported Crop Error
```json
{
  "error": "Unsupported crop type",
  "provided_crop": "InvalidCrop",
  "available_crops": ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Bajra"]
}
```

## 📊 Data Format Details

### Supported Crops
- **Wheat** - Price: ₹25/kg
- **Rice** - Price: ₹30/kg  
- **Cotton** - Price: ₹60/kg
- **Sugarcane** - Price: ₹3.5/kg
- **Maize** - Price: ₹20/kg
- **Bajra** - Price: ₹18/kg

### Coordinate Boundaries
- **Latitude:** 29.5° to 32.5° N (Punjab region)
- **Longitude:** 73.5° to 77.0° E (Punjab region)

### Farm Size Limits
- **Minimum:** 0.1 acres
- **Maximum:** 10,000 acres

## 🔧 Configuration

### Environment Variables
```bash
FLASK_APP=api_deploy.py
FLASK_ENV=production  # or development
```

### Production Deployment
```bash
# Using Gunicorn (recommended for production)
gunicorn -w 4 -b 0.0.0.0:5000 api_deploy:app

# Or with more workers for high traffic
gunicorn -w 8 -b 0.0.0.0:5000 --timeout 120 api_deploy:app
```

## 🚀 Integration Checklist

- [ ] API server is running and accessible
- [ ] Health check endpoint returns success
- [ ] Can fetch list of supported crops
- [ ] Successfully make prediction requests
- [ ] Handle API errors gracefully
- [ ] Validate coordinates before sending
- [ ] Display prediction results to users
- [ ] Show recommendations to farmers

## 📱 Mobile App Integration

For mobile apps, the same REST API can be used:

```javascript
// React Native example
const apiCall = async () => {
  try {
    const response = await fetch('http://your-server.com:5000/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(farmData)
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};
```

## 🔒 Security Notes

- API uses CORS to allow cross-origin requests
- Input validation prevents malicious data
- Rate limiting recommended for production
- HTTPS recommended for production deployment

## 📞 Support

For technical support or feature requests:
- Check API documentation at `/api/docs`
- Test endpoints with provided examples
- Validate input data format before sending requests

---

**🌾 Punjab Crop Advisory API v1.0.0**  
*AI-powered farming intelligence for Punjab*
