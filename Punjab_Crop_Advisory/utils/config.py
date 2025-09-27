import os
import json
from dotenv import load_dotenv

# Load .env file from project root (parent directory of utils)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '..', '.env')
load_dotenv(env_path)

class Config:
    """Configuration management"""
    
    # API Credentials
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Fix GEE path to work from both utils and notebooks directories
    _base_gee_path = os.getenv('GEE_SERVICE_ACCOUNT_JSON', 'config/google_earth_engine.json')
    if not os.path.exists(_base_gee_path):
        # Try from parent directory (for notebooks)
        _parent_gee_path = os.path.join('..', _base_gee_path)
        if os.path.exists(_parent_gee_path):
            GEE_SERVICE_ACCOUNT_JSON = _parent_gee_path
        else:
            GEE_SERVICE_ACCOUNT_JSON = _base_gee_path
    else:
        GEE_SERVICE_ACCOUNT_JSON = _base_gee_path
    
    # Project settings
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Punjab_Smart_Crop_Advisory')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    USE_FREE_WEATHER_BACKUP = os.getenv('USE_FREE_WEATHER_BACKUP', 'True').lower() == 'true'
    USE_SOILGRIDS_DATA = os.getenv('USE_SOILGRIDS_DATA', 'True').lower() == 'true'
    
    # Data paths
    DATA_DIR = 'data'
    RAW_DATA_DIR = f'{DATA_DIR}/raw'
    PROCESSED_DATA_DIR = f'{DATA_DIR}/processed'
    MODELS_DIR = 'models'
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GEE_SERVICE_ACCOUNT_JSON or not os.path.exists(cls.GEE_SERVICE_ACCOUNT_JSON):
            print(f"⚠️ GEE credential file not found: {cls.GEE_SERVICE_ACCOUNT_JSON}")
            return False
        return True
    
    @classmethod
    def create_directories(cls):
        """Create required directories"""
        dirs = [cls.RAW_DATA_DIR, cls.PROCESSED_DATA_DIR, cls.MODELS_DIR, 'logs']
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
        print("✅ All directories created")
