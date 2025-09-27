import ee
import json
import os
from config import Config

def initialize_earth_engine():
    """Initialize Google Earth Engine with your JSON credential"""
    
    print("🛰️ Initializing Google Earth Engine...")
    
    try:
        # Load your JSON credential file
        json_path = Config.GEE_SERVICE_ACCOUNT_JSON
        
        if not os.path.exists(json_path):
            print(f"❌ GEE JSON credential not found: {json_path}")
            print("📝 Please put your GEE JSON file in the config/ folder")
            return False
        
        # Load and parse the credential file
        with open(json_path, 'r') as f:
            key_data = json.load(f)
        
        # Extract service account email and project ID
        service_account_email = key_data['client_email']
        project_id = key_data.get('project_id', 'smart-crop-advisory')
        
        print(f"🔑 Service Account: {service_account_email}")
        print(f"🔑 Project ID: {project_id}")
        
        # Initialize with your credentials (optimized)
        credentials = ee.ServiceAccountCredentials(service_account_email, json_path)
        ee.Initialize(
            credentials=credentials,
            project=project_id,
            opt_url='https://earthengine.googleapis.com'
        )
        
        print(f"✅ Google Earth Engine initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Earth Engine initialization failed: {e}")
        print("💡 Make sure your JSON file is valid and has the right permissions")
        return False

def test_gee_access():
    """Test Google Earth Engine access with fast query"""
    
    try:
        # FAST TEST: Use simple number operation (instant)
        test_number = ee.Number(42).getInfo()
        
        if test_number == 42:
            print(f"✅ GEE Access Test: SUCCESS")
            print(f"🛰️ Earth Engine API is responding correctly")
            return True
        else:
            print(f"❌ GEE Access Test: FAILED - unexpected result: {test_number}")
            return False
        
    except Exception as e:
        print(f"❌ GEE Access Test: FAILED - {e}")
        return False

def test_gee_collections():
    """Optional: Test access to specific collections (slower but more thorough)"""
    
    try:
        # Test Sentinel-2 access without counting (much faster)
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        first_image = collection.first()
        image_id = first_image.get('system:id').getInfo()
        
        print(f"✅ Sentinel-2 Collection: Accessible")
        print(f"🛰️ Sample image ID: {image_id}")
        return True
        
    except Exception as e:
        print(f"❌ Collection Access Test: FAILED - {e}")
        return False

if __name__ == "__main__":
    if initialize_earth_engine():
        # Run fast basic test
        if test_gee_access():
            print("\n🔍 Running optional collection test...")
            test_gee_collections()
