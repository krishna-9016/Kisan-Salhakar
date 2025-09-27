# Punjab Crop Advisory - Port Configuration
===========================================

## 🔧 Updated Port Configuration (Avoiding 8000, 5000, 5173, 3005)

### 🚀 Main Services:

1. **Crop Prediction API Server**
   - **Port**: 9090
   - **URL**: http://localhost:9090
   - **API Docs**: http://localhost:9090/docs
   - **Health Check**: http://localhost:9090/health
   - **File**: crop_prediction_api.py

2. **FastAPI Backend Server** (Alternative)
   - **Port**: 9091
   - **URL**: http://localhost:9091
   - **API Docs**: http://localhost:9091/docs
   - **Health Check**: http://localhost:9091/health
   - **File**: fastapi_backend.py

3. **Flask Frontend Server**
   - **Port**: 7070
   - **URL**: http://localhost:7070
   - **File**: flask_frontend.py

### 🌐 Frontend Applications:

4. **Simple Frontend (HTML)**
   - **Type**: Static HTML file
   - **URL**: file:///path/to/simple_frontend.html
   - **Connects to**: http://localhost:9090 (Crop Prediction API)
   - **File**: simple_frontend.html

5. **Farmer Dashboard**
   - **Type**: Static HTML file
   - **URL**: file:///path/to/farmer_dashboard.html
   - **File**: farmer_dashboard.html

### 🔑 API Configuration:

- **Primary API Key**: punjab_crop_api_2024
- **Authentication**: Bearer token in Authorization header
- **CORS**: Enabled for all origins (development mode)

### 🎯 Usage:

1. **Start Main API Server**:
   ```bash
   cd Punjab_Crop_Advisory
   python crop_prediction_api.py
   ```
   → Server starts on port 9090

2. **Start Flask Frontend** (Optional):
   ```bash
   cd Punjab_Crop_Advisory
   python flask_frontend.py
   ```
   → Server starts on port 7070

3. **Use Simple Frontend**:
   - Open simple_frontend.html in browser
   - Automatically connects to API on port 9090

### ✅ Port Availability:
- ✅ Port 9090 - Crop Prediction API
- ✅ Port 9091 - FastAPI Backend (alternative)
- ✅ Port 7070 - Flask Frontend
- ❌ Port 8000 - AVOIDED (common development port)
- ❌ Port 5000 - AVOIDED (Flask default)
- ❌ Port 5173 - AVOIDED (Vite default)
- ❌ Port 3005 - AVOIDED (React/Node common port)

### 🔧 Testing:

1. **Health Check**: GET http://localhost:9090/health
2. **API Documentation**: http://localhost:9090/docs
3. **Frontend Test**: Open simple_frontend.html and click "Test API Connection"

### 📝 Notes:

- All components now use unique ports avoiding conflicts
- Frontend automatically connects to the correct API port
- API key authentication is enabled
- CORS is configured for frontend integration
- Server logs show successful startup and health checks
