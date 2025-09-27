@echo off
echo 🌾 Punjab Crop Advisory System - Enhanced Version
echo ================================================
echo Starting API Server and Frontend...
echo.

echo 🚀 Starting API Server on port 9090...
start "API Server" cmd /k "cd /d %~dp0 && python crop_prediction_api.py"

timeout /t 5 /nobreak >nul

echo 🌐 Starting Frontend Server on port 6060...
start "Frontend Server" cmd /k "cd /d %~dp0 && python start_frontend_server.py"

echo.
echo ✅ Both servers are starting...
echo 📊 API Server: http://localhost:9090
echo 🌐 Frontend: http://localhost:6060/simple_frontend.html
echo.
echo Features:
echo   ✅ Crop yield prediction
echo   ✅ Alternative crop recommendations  
echo   ✅ Farming tips and advice
echo   ✅ Seasonal guidance
echo   ✅ Profitability analysis
echo.
echo Press any key to open the frontend...
pause >nul
start http://localhost:6060/simple_frontend.html
