#!/usr/bin/env python3
"""
Enhanced API Test - Test the new crop recommendations and farming tips
"""

import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:9090"
API_KEY = "punjab_crop_api_2024"

def test_enhanced_prediction():
    """Test the enhanced prediction with recommendations"""
    
    print("🧪 Enhanced Punjab Crop API Test")
    print("=" * 50)
    
    # Test data
    test_data = {
        "crop": "wheat",
        "acres": 10.0,
        "latitude": 30.7333,
        "longitude": 76.7794
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("\n🌾 Testing enhanced prediction...")
        print(f"📤 Sending request: {test_data}")
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/predict",
            headers=headers,
            json=test_data
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced prediction successful!\n")
            
            # Print main prediction
            print(f"🌾 Current Crop ({data['user_input']['crop'].title()}):")
            print(f"   Predicted Yield: {data['predicted_yield']:.2f} kg/acre")
            print(f"   Confidence: {data['confidence']}")
            print(f"   Range: {data['yield_range']['minimum']:.1f} - {data['yield_range']['maximum']:.1f} kg/acre")
            
            # Print crop recommendations
            if 'crop_recommendations' in data and data['crop_recommendations']:
                print(f"\n🌱 Alternative Crop Recommendations:")
                for i, rec in enumerate(data['crop_recommendations'], 1):
                    print(f"\n   {i}. {rec['crop_name']}")
                    print(f"      Suitability Score: {rec['suitability_score']:.2f}")
                    print(f"      Expected Yield: {rec['expected_yield']:.1f} kg/acre")
                    print(f"      Profitability: {rec['profitability']}")
                    print(f"      Why choose:")
                    for reason in rec['reasons']:
                        print(f"        • {reason}")
                    print(f"      Growing tips:")
                    for tip in rec['tips']:
                        print(f"        💡 {tip}")
            
            # Print farming tips
            if 'farming_tips' in data and data['farming_tips']:
                print(f"\n🚜 General Farming Tips:")
                for tip in data['farming_tips']:
                    print(f"   💡 {tip}")
            
            # Print seasonal advice
            if 'seasonal_advice' in data and data['seasonal_advice']:
                print(f"\n📅 Seasonal Advice:")
                print(f"   {data['seasonal_advice']}")
            
            print(f"\n📊 Technical Details:")
            print(f"   Season: {data['estimated_parameters']['season']}")
            print(f"   Temperature: {data['estimated_parameters']['temperature']}")
            print(f"   Humidity: {data['estimated_parameters']['humidity']}")
            print(f"   Model: {data['model_info']['model_type']}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_enhanced_prediction()
