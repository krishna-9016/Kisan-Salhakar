# 🌾 Punjab Crop Advisory - Frontend Integration Guide

## 📋 Overview
This guide will help you integrate the **Punjab Crop Advisory API** with your existing React frontend. Your friend has built a sophisticated crop prediction system that provides yield predictions, farming recommendations, and agricultural insights based on location, crop type, and farm size.

## 🎯 What Your Frontend Already Has vs What You Need

### ✅ Your Current Frontend Features:
- Location selection (map + coordinates)
- Crop type selection
- Farm size input
- Location Advisory Page with map interface
- React + Material UI setup
- Leaflet maps integration

### 🚀 What the Crop Advisory API Will Add:
- **AI-powered crop yield predictions** (kg/acre)
- **Crop recommendations** based on location and season
- **Farming tips** and seasonal advice
- **Weather and soil data** analysis
- **Economic projections** (revenue estimates)
- **Alternative crop suggestions**

## 📁 Project Structure Overview

```
SIH2/
├── frontend/                    # Your React app
│   ├── src/pages/
│   │   └── LocationAdvisoryPage.jsx  # WHERE TO INTEGRATE
│   └── package.json
├── backend/                     # Your existing backend
└── Punjab_Crop_Advisory/        # Crop prediction system
    ├── crop_prediction_api.py   # Main API server
    ├── fastapi_backend.py       # Alternative API
    └── models/                  # ML models
```

## 🔧 Step-by-Step Integration

### Step 1: Start the Crop Advisory API

Navigate to the Punjab_Crop_Advisory folder and start the API:

```bash
# Open terminal in Punjab_Crop_Advisory folder
cd C:\Users\DELL\OneDrive\Desktop\SIH2\Punjab_Crop_Advisory

# Start the crop prediction API
python crop_prediction_api.py
```

**API will be available at:** `http://localhost:9090`

### Step 2: Install Required Frontend Dependencies

Your frontend already has axios, so no additional packages needed!

### Step 3: Create API Service File

Create a new file: `frontend/src/services/cropAdvisoryApi.js`

```javascript
import axios from 'axios';

const CROP_API_BASE_URL = 'http://localhost:9090';
const API_KEY = 'punjab_crop_api_2024';

// Create axios instance with default config
const cropApiClient = axios.create({
  baseURL: CROP_API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
});

export const cropAdvisoryService = {
  // Get crop yield prediction and recommendations
  async getCropPrediction(locationData) {
    try {
      const response = await cropApiClient.post('/api/v1/predict', {
        crop: locationData.crop,
        acres: locationData.farmSize,
        latitude: locationData.latitude,
        longitude: locationData.longitude
      });
      return response.data;
    } catch (error) {
      console.error('Crop prediction failed:', error);
      throw new Error(error.response?.data?.detail || 'Failed to get crop prediction');
    }
  },

  // Get supported crops list
  async getSupportedCrops() {
    try {
      const response = await cropApiClient.get('/api/v1/crops');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch crops:', error);
      throw error;
    }
  },

  // Get Punjab districts
  async getPunjabDistricts() {
    try {
      const response = await cropApiClient.get('/api/v1/districts');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch districts:', error);
      throw error;
    }
  },

  // Health check
  async checkApiHealth() {
    try {
      const response = await cropApiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('API health check failed:', error);
      return { status: 'unavailable' };
    }
  }
};
```

### Step 4: Update LocationAdvisoryPage.jsx

Replace the existing `handleGetAdvisory` function and add crop/farm size inputs:

```javascript
import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Button, Paper, CircularProgress, Alert, 
  MenuItem, Select, InputLabel, FormControl, TextField,
  Card, CardContent, Chip, List, ListItem, ListItemText
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';
import { cropAdvisoryService } from '../services/cropAdvisoryApi';
import './LocationAdvisoryPage.css';

// ... (keep existing punjabLocations, punjabCenter, etc.)

const LocationAdvisoryPage = () => {
  const navigate = useNavigate();
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedCity, setSelectedCity] = useState("");
  const [mapCenter, setMapCenter] = useState(punjabCenter);
  const [loading, setLoading] = useState(false);
  
  // New states for crop advisory
  const [selectedCrop, setSelectedCrop] = useState("");
  const [farmSize, setFarmSize] = useState("");
  const [supportedCrops, setSupportedCrops] = useState([]);
  const [predictionResult, setPredictionResult] = useState(null);
  const [apiError, setApiError] = useState(null);

  // Load supported crops on component mount
  useEffect(() => {
    const loadSupportedCrops = async () => {
      try {
        const cropsData = await cropAdvisoryService.getSupportedCrops();
        setSupportedCrops(cropsData.crops || []);
      } catch (error) {
        console.error('Failed to load crops:', error);
        // Fallback crops list
        setSupportedCrops(['wheat', 'rice', 'cotton', 'maize', 'sugarcane']);
      }
    };
    loadSupportedCrops();
  }, []);

  // Updated handleGetAdvisory function
  const handleGetAdvisory = async () => {
    if (!selectedLocation || !selectedCrop || !farmSize) {
      setApiError('Please select location, crop type, and enter farm size');
      return;
    }

    setLoading(true);
    setApiError(null);
    setPredictionResult(null);

    try {
      const locationData = {
        latitude: selectedLocation.lat,
        longitude: selectedLocation.lng,
        crop: selectedCrop,
        farmSize: parseFloat(farmSize)
      };

      const result = await cropAdvisoryService.getCropPrediction(locationData);
      setPredictionResult(result);
    } catch (error) {
      setApiError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // ... (keep existing map handlers)

  return (
    <div className="location-advisory-container">
      <header className="location-advisory-header">
        <Typography variant="h4" component="h1">🌾 Smart Crop Advisory</Typography>
        <Button variant="outlined" onClick={() => navigate('/')}>Back to Home</Button>
      </header>

      <main className="location-advisory-main-content">
        <div className="map-panel">
          <MapContainer center={mapCenter} zoom={9} className="full-height-map">
            <ChangeView center={mapCenter} zoom={10} />
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MapClickHandler onMapClick={handleMapClick} />
            {selectedLocation && <Marker position={selectedLocation} />}
          </MapContainer>
        </div>

        <div className="advisory-panel">
          <Paper elevation={3} sx={{ padding: '24px', borderRadius: '12px', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h5" gutterBottom>🌾 Crop Advisory Analysis</Typography>

            {/* Location Selection */}
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select District</InputLabel>
              <Select
                value={selectedCity}
                label="Select District"
                onChange={handleCityChange}
              >
                {Object.keys(punjabLocations).map(city => (
                  <MenuItem key={city} value={city}>{city}</MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Crop Selection */}
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select Crop Type</InputLabel>
              <Select
                value={selectedCrop}
                label="Select Crop Type"
                onChange={(e) => setSelectedCrop(e.target.value)}
              >
                {supportedCrops.map(crop => (
                  <MenuItem key={crop} value={crop}>
                    {crop.charAt(0).toUpperCase() + crop.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Farm Size Input */}
            <TextField
              fullWidth
              label="Farm Size (acres)"
              type="number"
              value={farmSize}
              onChange={(e) => setFarmSize(e.target.value)}
              inputProps={{ min: 0.1, max: 10000, step: 0.1 }}
              sx={{ mb: 2 }}
              helperText="Enter your farm size in acres"
            />

            {/* Error Display */}
            {apiError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {apiError}
              </Alert>
            )}
            
            <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              {!selectedLocation && (
                <Alert severity="info">📍 Click on the map or select a district to begin.</Alert>
              )}
              
              {selectedLocation && !predictionResult && !loading && (
                <Box sx={{ textAlign: 'center' }}>
                  <Typography gutterBottom>
                    📍 Location: {selectedCity || `${selectedLocation.lat.toFixed(4)}, ${selectedLocation.lng.toFixed(4)}`}
                  </Typography>
                  {selectedCrop && (
                    <Typography gutterBottom>
                      🌾 Crop: {selectedCrop.charAt(0).toUpperCase() + selectedCrop.slice(1)}
                    </Typography>
                  )}
                  {farmSize && (
                    <Typography gutterBottom>
                      📏 Farm Size: {farmSize} acres
                    </Typography>
                  )}
                  <Button 
                    variant="contained" 
                    size="large" 
                    onClick={handleGetAdvisory} 
                    disabled={loading || !selectedCrop || !farmSize}
                    sx={{ mt: 2 }}
                  >
                    {loading ? <CircularProgress size={24} color="inherit" /> : '🚀 Get AI Prediction'}
                  </Button>
                </Box>
              )}

              {loading && (
                <Box sx={{display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center'}}>
                  <CircularProgress sx={{ mb: 2 }} />
                  <Typography>Analyzing crop data...</Typography>
                </Box>
              )}

              {/* Prediction Results */}
              {predictionResult && (
                <div className="prediction-results" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  {/* Yield Prediction */}
                  <Card sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" color="primary">📊 Yield Prediction</Typography>
                      <Typography variant="h4" color="success.main" sx={{ my: 1 }}>
                        {predictionResult.predicted_yield} kg/acre
                      </Typography>
                      <Typography variant="body2">
                        Range: {predictionResult.yield_range.minimum} - {predictionResult.yield_range.maximum} kg/acre
                      </Typography>
                      <Chip 
                        label={`${predictionResult.confidence} Confidence`} 
                        color={predictionResult.confidence === 'High' ? 'success' : 'warning'}
                        size="small"
                        sx={{ mt: 1 }}
                      />
                    </CardContent>
                  </Card>

                  {/* Crop Recommendations */}
                  <Card sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" color="primary" gutterBottom>
                        🌱 Alternative Crop Recommendations
                      </Typography>
                      {predictionResult.crop_recommendations?.slice(0, 3).map((rec, index) => (
                        <Box key={index} sx={{ mb: 1, p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
                          <Typography variant="subtitle2" fontWeight="bold">
                            {rec.crop_name} - {rec.profitability} Profitability
                          </Typography>
                          <Typography variant="body2">
                            Expected: {rec.expected_yield} kg/acre
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {rec.reasons[0]}
                          </Typography>
                        </Box>
                      ))}
                    </CardContent>
                  </Card>

                  {/* Farming Tips */}
                  <Card sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6" color="primary" gutterBottom>
                        💡 Farming Tips
                      </Typography>
                      <List dense>
                        {predictionResult.farming_tips?.slice(0, 4).map((tip, index) => (
                          <ListItem key={index} sx={{ py: 0.5 }}>
                            <ListItemText 
                              primary={tip}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>

                  {/* Seasonal Advice */}
                  <Card>
                    <CardContent>
                      <Typography variant="h6" color="primary" gutterBottom>
                        🗓️ Seasonal Advice
                      </Typography>
                      <Typography variant="body2">
                        {predictionResult.seasonal_advice}
                      </Typography>
                    </CardContent>
                  </Card>
                </div>
              )}
            </Box>
          </Paper>
        </div>
      </main>
    </div>
  );
};

export default LocationAdvisoryPage;
```

### Step 5: Test the Integration

1. **Start both servers:**
   ```bash
   # Terminal 1: Start Punjab Crop Advisory API
   cd Punjab_Crop_Advisory
   python crop_prediction_api.py

   # Terminal 2: Start your React frontend
   cd frontend
   npm run dev
   ```

2. **Test the integration:**
   - Navigate to Location Advisory page
   - Click on map to select location
   - Choose a crop type (wheat, rice, etc.)
   - Enter farm size in acres
   - Click "Get AI Prediction"

### Step 6: Customize the UI (Optional)

Add these CSS styles to `LocationAdvisoryPage.css`:

```css
.prediction-results {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.map-panel {
  flex: 1;
  min-height: 500px;
}

.advisory-panel {
  flex: 1;
  min-width: 400px;
}

.location-advisory-main-content {
  display: flex;
  gap: 20px;
  height: calc(100vh - 120px);
}

@media (max-width: 768px) {
  .location-advisory-main-content {
    flex-direction: column;
    height: auto;
  }
  
  .map-panel, .advisory-panel {
    min-height: 400px;
  }
}
```

## 🚀 API Endpoints Reference

### Main Prediction Endpoint
```
POST http://localhost:9090/api/v1/predict
```

**Request Body:**
```json
{
  "crop": "wheat",
  "acres": 5.0,
  "latitude": 30.9010,
  "longitude": 75.8573
}
```

**Response:**
```json
{
  "success": true,
  "predicted_yield": 1845.2,
  "yield_range": {
    "minimum": 1568.4,
    "maximum": 2122.0
  },
  "confidence": "High",
  "crop_recommendations": [...],
  "farming_tips": [...],
  "seasonal_advice": "...",
  "estimated_parameters": {...}
}
```

### Other Useful Endpoints
- `GET /health` - Check API status
- `GET /api/v1/crops` - Get supported crops
- `GET /api/v1/districts` - Get Punjab districts

## 🔧 Troubleshooting

### Common Issues:

1. **API not responding:**
   ```bash
   # Check if API is running
   curl http://localhost:9090/health
   ```

2. **CORS errors:**
   - The API already has CORS enabled
   - Make sure you're using the correct port (9090)

3. **Authentication errors:**
   - API key is hardcoded as `punjab_crop_api_2024`
   - Check the Authorization header in your requests

4. **Model not loading:**
   - Check if `punjab_crop_yield_predictor_final.pkl` exists in the models folder
   - API will use a demo model if main model isn't found

### Testing Commands:

```bash
# Test API health
curl http://localhost:9090/health

# Test prediction
curl -X POST http://localhost:9090/api/v1/predict \
  -H "Authorization: Bearer punjab_crop_api_2024" \
  -H "Content-Type: application/json" \
  -d '{"crop":"wheat","acres":5,"latitude":30.9,"longitude":75.8}'

# Test crops list
curl -H "Authorization: Bearer punjab_crop_api_2024" \
  http://localhost:9090/api/v1/crops
```

## 📈 Features You Now Have

After integration, your Location Advisory page will provide:

✅ **AI-Powered Predictions:** Machine learning-based crop yield predictions  
✅ **Smart Recommendations:** Alternative crops suited for the location  
✅ **Farming Tips:** Actionable agricultural advice  
✅ **Seasonal Guidance:** Time-specific farming recommendations  
✅ **Economic Insights:** Yield ranges and confidence levels  
✅ **Weather & Soil Data:** Environmental parameter analysis  

## 🎯 Next Steps

1. **Start the API server** (`python crop_prediction_api.py`)
2. **Create the API service file** (`cropAdvisoryApi.js`)
3. **Update LocationAdvisoryPage.jsx** with the new code
4. **Test the integration** thoroughly
5. **Customize the UI** to match your design

## 🔗 Deployment Notes

For production deployment:

1. **API Server:** Deploy the Punjab_Crop_Advisory API on a cloud server
2. **Update Base URL:** Change `CROP_API_BASE_URL` to your production API URL
3. **Environment Variables:** Store API keys in environment variables
4. **Error Handling:** Add comprehensive error handling for production use

## 📞 Support

If you encounter any issues:
1. Check that both servers are running
2. Verify the API key is correct
3. Test API endpoints with curl first
4. Check browser console for errors
5. Ensure coordinates are within Punjab boundaries (lat: 29.5-32.5, lng: 73.5-77.0)

---

**🎉 Congratulations!** Your frontend now has AI-powered crop advisory capabilities. The system will provide intelligent farming recommendations based on location, crop type, and farm size, making your agricultural platform much more valuable to farmers.
