# Punjab Crop Prediction API Documentation

## Overview
The Punjab Crop Prediction API provides AI-powered crop yield predictions for Punjab agriculture. This standalone API service is designed for easy integration into larger UI projects.

## API Information
- **Base URL**: `http://localhost:8000`
- **Authentication**: Bearer Token (API Key)
- **Content-Type**: `application/json`
- **Version**: 1.0.0

## API Keys
```
crop_predict_2024   - Main API key for production
punjab_agri_api     - Secondary API key
demo_api_key        - Demo/testing key
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check API health status (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "RandomForestRegressor",
  "timestamp": "2024-09-07T10:30:00",
  "api_version": "1.0.0"
}
```

### 2. Crop Yield Prediction
**POST** `/api/v1/predict`

Predict crop yield based on farm parameters.

**Headers:**
```
Authorization: Bearer crop_predict_2024
Content-Type: application/json
```

**Request Body:**
```json
{
  "crop": "wheat",
  "district": "Amritsar",
  "farm_size_acres": 10.5,
  "latitude": 31.6340,
  "longitude": 75.8573,
  "year": 2024,
  "season": "rabi"
}
```

**Required Fields:**
- `crop` (string): Crop type
- `district` (string): Punjab district name
- `farm_size_acres` (float): Farm size in acres
- `latitude` (float): Farm latitude (29.0-33.0)
- `longitude` (float): Farm longitude (73.0-77.0)

**Optional Fields:**
- `year` (int): Year (defaults to current year)
- `season` (string): Season (auto-detected if not provided)

**Response:**
```json
{
  "success": true,
  "predicted_yield": 1850.5,
  "yield_range": {
    "minimum": 1572.9,
    "maximum": 2128.1
  },
  "confidence": "High",
  "user_input": {
    "crop": "wheat",
    "district": "Amritsar",
    "farm_size_acres": 10.5,
    "latitude": 31.6340,
    "longitude": 75.8573
  },
  "estimated_parameters": {
    "season": "rabi",
    "temperature": "22.3°C",
    "humidity": "68.4%",
    "rainfall": "560mm",
    "soil_pH": 7.1
  },
  "model_info": {
    "model_type": "RandomForestRegressor",
    "version": "1.0.0",
    "units": "kg/acre"
  },
  "api_version": "1.0.0",
  "timestamp": "2024-09-07T10:30:00"
}
```

### 3. Get Supported Crops
**GET** `/api/v1/crops`

Get list of supported crops.

**Headers:**
```
Authorization: Bearer crop_predict_2024
```

**Response:**
```json
{
  "crops": ["wheat", "rice", "corn", "maize", "cotton", "soybean"],
  "rabi_crops": ["wheat", "barley", "mustard", "potato"],
  "kharif_crops": ["rice", "corn", "maize", "cotton", "soybean"]
}
```

### 4. Get Punjab Districts
**GET** `/api/v1/districts`

Get list of supported Punjab districts.

**Headers:**
```
Authorization: Bearer crop_predict_2024
```

**Response:**
```json
{
  "districts": [
    "Amritsar", "Ludhiana", "Jalandhar", "Patiala", 
    "Bathinda", "Mohali", "Gurdaspur", "..."
  ]
}
```

## Frontend Integration Examples

### JavaScript/Fetch
```javascript
async function predictCropYield(farmData) {
    const response = await fetch('http://localhost:8000/api/v1/predict', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer crop_predict_2024',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            crop: farmData.crop,
            district: farmData.district,
            farm_size_acres: farmData.farmSize,
            latitude: farmData.latitude,
            longitude: farmData.longitude
        })
    });
    
    return await response.json();
}

// Usage
const result = await predictCropYield({
    crop: 'wheat',
    district: 'Amritsar',
    farmSize: 10.5,
    latitude: 31.6340,
    longitude: 75.8573
});

console.log(`Predicted yield: ${result.predicted_yield} kg/acre`);
```

### React Component
```jsx
import React, { useState } from 'react';

const CropPrediction = () => {
    const [prediction, setPrediction] = useState(null);
    
    const predictYield = async (formData) => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/predict', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer crop_predict_2024',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            setPrediction(result);
        } catch (error) {
            console.error('Prediction failed:', error);
        }
    };
    
    return (
        <div>
            {prediction && (
                <div>
                    <h3>Yield: {prediction.predicted_yield} kg/acre</h3>
                    <p>Confidence: {prediction.confidence}</p>
                </div>
            )}
        </div>
    );
};
```

### Python Client
```python
import requests

class CropPredictionClient:
    def __init__(self, api_url="http://localhost:8000", api_key="crop_predict_2024"):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def predict_yield(self, crop, district, farm_size_acres, latitude, longitude):
        data = {
            "crop": crop,
            "district": district,
            "farm_size_acres": farm_size_acres,
            "latitude": latitude,
            "longitude": longitude
        }
        
        response = requests.post(
            f"{self.api_url}/api/v1/predict",
            headers=self.headers,
            json=data
        )
        
        return response.json()

# Usage
client = CropPredictionClient()
result = client.predict_yield("wheat", "Amritsar", 10.5, 31.6340, 75.8573)
print(f"Predicted yield: {result['predicted_yield']} kg/acre")
```

## Error Handling

### Authentication Errors
```json
{
  "detail": "Invalid API key",
  "status_code": 401
}
```

### Validation Errors
```json
{
  "detail": [
    {
      "loc": ["body", "latitude"],
      "msg": "ensure this value is greater than or equal to 29.0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### Server Errors
```json
{
  "detail": "Prediction failed: Model not available"
}
```

## Smart Parameter Estimation

The API automatically estimates weather and soil parameters based on:

- **Location**: Latitude/longitude coordinates
- **Crop Type**: Rabi vs Kharif classification
- **District**: Regional variations
- **Season**: Automatic detection based on crop

**Estimated Parameters:**
- Temperature, humidity, rainfall, wind speed
- Soil pH, organic carbon, NPK nutrients
- Satellite data (NDVI, spectral bands)
- Sowing month and season

## Rate Limits
- **Default**: 100 requests per minute per API key
- **Burst**: Up to 10 concurrent requests

## Production Deployment
1. Change API keys for security
2. Configure CORS for specific domains
3. Add rate limiting middleware
4. Use HTTPS in production
5. Monitor API usage and performance

## Support
For integration support or issues:
- Check API health endpoint
- Validate request format
- Verify API key permissions
- Review error responses
