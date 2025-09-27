#!/usr/bin/env python3
"""
API Test Script
===============
Test the Punjab Crop Prediction API to ensure it's working correctly
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:9090"
API_KEY = "punjab_crop_api_2024"

def test_health_check():
    """Test the health endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("\n🌾 Testing crop prediction...")
    
    # Test data
    test_data = {
        "crop": "wheat",
        "acres": 5.0,
        "latitude": 30.7333,
        "longitude": 76.7794
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        print(f"📤 Sending request: {test_data}")
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict", 
            json=test_data, 
            headers=headers
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction successful!")
            print(f"🌾 Predicted Yield: {data['predicted_yield']:.2f} kg/acre")
            print(f"🎯 Confidence: {data['confidence']}")
            print(f"📊 Range: {data['yield_range']['minimum']:.1f} - {data['yield_range']['maximum']:.1f} kg/acre")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def main():
    print("🧪 Punjab Crop API Test Suite")
    print("=" * 40)
    
    # Test health check
    health_ok = test_health_check()
    
    # Test prediction
    prediction_ok = test_prediction()
    
    print("\n📋 Test Results:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Prediction: {'✅ PASS' if prediction_ok else '❌ FAIL'}")
    
    if health_ok and prediction_ok:
        print("\n🎉 All tests passed! API is working correctly.")
        print("🌐 Frontend should now work at: http://localhost:6060/simple_frontend.html")
    else:
        print("\n❌ Some tests failed. Check the API server.")

if __name__ == "__main__":
    main()
