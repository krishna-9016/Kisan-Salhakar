@echo off
echo ==============================================
echo  Punjab Crop Yield Predictor - Quick Start
echo ==============================================
echo.

echo Step 1: Installing Python packages...
pip install -r requirements_simple.txt

echo.
echo Step 2: Starting FastAPI backend server...
echo.
echo IMPORTANT: Save the API key that appears below!
echo You'll need it for the frontend.
echo.
echo After the server starts:
echo 1. Open 'frontend_example.html' in your browser
echo 2. Use the API key shown below
echo 3. Click 'Get Prediction' to test!
echo.
echo ============================================
echo Starting server now...
echo ============================================

python fastapi_backend.py

pause
