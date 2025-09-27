import requests
import pandas as pd
import numpy as np
from datetime import datetime
from config import Config

class WeatherAPI:
    """Weather data from OpenWeatherMap + Free backup"""
    
    def __init__(self):
        self.openweather_key = Config.OPENWEATHER_API_KEY
        self.openweather_url = "http://api.openweathermap.org/data/2.5"
        self.free_weather_url = "https://api.open-meteo.com/v1"
        
    def get_weather_openweather(self, lat, lon):
        """Get weather from OpenWeatherMap (your API key)"""
        
        if not self.openweather_key:
            return None
        
        try:
            url = f"{self.openweather_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'rainfall': data.get('rain', {}).get('1h', 0),
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'weather_description': data['weather'][0]['description'],
                'data_source': 'OpenWeatherMap',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"OpenWeatherMap error: {e}")
            return None
    
    def get_weather_free_backup(self, lat, lon):
        """Get weather from Open-Meteo (FREE, no API key required)"""
        
        try:
            url = f"{self.free_weather_url}/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': ['temperature_2m', 'relative_humidity_2m', 'precipitation', 
                           'wind_speed_10m', 'wind_direction_10m', 'surface_pressure'],
                'timezone': 'Asia/Kolkata'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            
            return {
                'temperature': current['temperature_2m'],
                'humidity': current['relative_humidity_2m'],
                'pressure': current.get('surface_pressure', 1013),
                'rainfall': current.get('precipitation', 0),
                'wind_speed': current['wind_speed_10m'],
                'wind_direction': current.get('wind_direction_10m', 0),
                'weather_description': 'clear sky',
                'data_source': 'Open-Meteo_Free',
                'timestamp': current['time']
            }
            
        except Exception as e:
            print(f"Free weather API error: {e}")
            return self._generate_punjab_weather(lat, lon)
    
    def get_weather_for_location(self, lat, lon):
        """Get weather with fallback strategy"""
        
        # Try OpenWeatherMap first
        weather = self.get_weather_openweather(lat, lon)
        
        # If failed, try free backup
        if weather is None:
            weather = self.get_weather_free_backup(lat, lon)
        
        # If both failed, generate synthetic
        if weather is None:
            weather = self._generate_punjab_weather(lat, lon)
        
        return weather
    
    def _generate_punjab_weather(self, lat, lon):
        """Generate realistic Punjab weather as last resort"""
        
        np.random.seed(int((lat + lon) * 1000) % 1000)
        
        # Punjab seasonal weather patterns
        month = datetime.now().month
        
        if month in [12, 1, 2]:  # Winter
            temp_range = (8, 22)
            humidity_range = (60, 85)
            rain_prob = 0.15
        elif month in [3, 4, 5]:  # Summer
            temp_range = (25, 45)
            humidity_range = (30, 60)
            rain_prob = 0.05
        elif month in [6, 7, 8, 9]:  # Monsoon
            temp_range = (28, 38)
            humidity_range = (70, 95)
            rain_prob = 0.60
        else:  # Post-monsoon
            temp_range = (18, 32)
            humidity_range = (50, 75)
            rain_prob = 0.20
        
        return {
            'temperature': np.random.uniform(*temp_range),
            'humidity': np.random.uniform(*humidity_range),
            'pressure': np.random.normal(1013, 15),
            'rainfall': np.random.exponential(3) if np.random.random() < rain_prob else 0,
            'wind_speed': np.random.normal(8, 3),
            'wind_direction': np.random.uniform(0, 360),
            'weather_description': 'partly cloudy',
            'data_source': 'Punjab_Synthetic_Model',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_weather_for_multiple_locations(self, locations_df):
        """Get weather for all farm plots"""
        
        weather_data = []
        
        print("🌤️ Collecting weather data...")
        
        for _, row in locations_df.iterrows():
            weather = self.get_weather_for_location(row['latitude'], row['longitude'])
            weather['plot_id'] = row['plot_id']
            weather_data.append(weather)
        
        df = pd.DataFrame(weather_data)
        print(f"✅ Weather data collected for {len(df)} locations")
        print(f"📊 Data sources used: {df['data_source'].value_counts().to_dict()}")
        
        return df

# Global instance
weather_api = WeatherAPI()
if __name__ == "__main__":
    # Example usage
    api = WeatherAPI()
    sample_weather = api.get_weather_for_location(30.901, 75.857)  # Ludhiana coordinates
    print(sample_weather)