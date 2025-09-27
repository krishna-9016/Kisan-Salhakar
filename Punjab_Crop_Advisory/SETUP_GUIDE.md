# 🌾 Punjab Crop Yield Predictor - Setup Guide

## 📋 Project Overview
This is an AI-powered crop yield prediction system for Punjab farmers using FastAPI backend with a trained RandomForest ML model and a simple HTML frontend.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+ installed
- Internet connection for installing packages

### Step 1: Setup Python Environment
```bash
# Navigate to project directory
cd Punjab_Crop_Advisory

# Install required packages
pip install -r requirements.txt
```

### Step 2: Start the Backend Server
```bash
# Run the FastAPI backend
python fastapi_backend.py
```

**Important:** When the server starts, you'll see an API key printed in the console like:
```
🔑 Generated NEW API Key: abc123xyz...
```
**Save this API key!** You'll need it for the frontend.

### Step 3: Open the Frontend
1. Open `frontend_example.html` in your web browser
2. The API key should be pre-filled, but if not, paste the key from Step 2
3. Click "Get Prediction" to test!

## 📁 Project Structure

```
Punjab_Crop_Advisory/
├── fastapi_backend.py          # Main API server
├── frontend_example.html       # Web interface
├── models/                     # Trained ML models
│   ├── punjab_crop_yield_predictor_final.pkl
│   └── prediction_function.py
├── data/                       # Training data and processed files
├── requirements.txt            # Python dependencies
└── SETUP_GUIDE.md             # This file
```

## 🔧 Detailed Setup Instructions

### Method 1: Using Anaconda (Recommended)
```bash
# Create new environment
conda create -n crop_predictor python=3.9
conda activate crop_predictor

# Install packages
pip install -r requirements.txt

# Run the server
python fastapi_backend.py
```

### Method 2: Using Virtual Environment
```bash
# Create virtual environment
python -m venv crop_env

# Activate environment
# Windows:
crop_env\Scripts\activate
# Linux/Mac:
source crop_env/bin/activate

# Install packages
pip install -r requirements.txt

# Run the server
python fastapi_backend.py
```

## 🌐 Using the Application

### Backend (FastAPI Server)
- **URL:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Frontend (Web Interface)
1. Open `frontend_example.html` in any modern web browser
2. Enter the API key from the backend console
3. Fill in farm details:
   - **Longitude:** 75.8573 (example for Punjab)
   - **Latitude:** 30.9010 (example for Punjab)
   - **Crop:** Select from dropdown (wheat, rice, corn, cotton, soybean)
   - **Farm Size:** Enter in acres (e.g., 5.0)
4. Click "Get Prediction"

### Sample Prediction Output
```json
{
  "prediction": "563.4 kg/acre for wheat",
  "input": {
    "latitude": 30.9010,
    "longitude": 75.8573,
    "crop": "wheat",
    "farm_size_acres": 5.0
  },
  "model_info": {
    "model_type": "RandomForestRegressor"
  },
  "timestamp": "2025-09-05T12:44:00"
}
```

## 📦 Package Contents

### Core Files (Essential)
- `fastapi_backend.py` - Main API server
- `frontend_example.html` - Web interface  
- `requirements.txt` - Python dependencies
- `models/` - Trained ML models and prediction logic
- `data/processed/` - Processed datasets for model

### Additional Files
- `data/raw/` - Original training data
- `notebooks/` - Jupyter notebooks for model development
- `docs/` - Additional documentation
- `scripts/` - Utility scripts

## 🔑 API Key Information
- New API key is generated each time you start the server
- The key is displayed in the console when the server starts
- For security, the key changes on every restart
- Current key is saved in `.api_key` file (don't share this file)

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. "Port already in use" error**
- Stop any existing servers
- Or change port in `fastapi_backend.py` (line with `uvicorn.run`)

**3. "API key invalid" error**
- Copy the exact API key from the backend console
- Make sure there are no extra spaces

**4. "Model file not found" error**
- Ensure `models/` directory exists with `.pkl` files
- Re-run model training if needed

### Getting Help
1. Check the console output for detailed error messages
2. Ensure all files from the package are present
3. Verify Python version is 3.8+

## 🔧 Development Notes

### Model Information
- **Algorithm:** RandomForestRegressor
- **Features:** 39 features including location, weather, soil data
- **Target:** Crop yield in kg/acre
- **Training Data:** Punjab agricultural dataset

### API Endpoints
- `GET /health` - Server health check
- `POST /predict` - Make crop yield prediction
- `GET /docs` - API documentation

### Technologies Used
- **Backend:** FastAPI, scikit-learn, pandas, numpy
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **ML Model:** RandomForest trained on Punjab crop data

## 📞 Support
If you encounter any issues:
1. Check this guide first
2. Look at console error messages
3. Ensure all dependencies are installed
4. Make sure model files are present

---
**Happy Farming! 🌾**
