# Punjab Crop Advisory - Data Collection Module
# Converted from 01_Data_Collection_Complete.ipynb

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add utils to path
current_dir = os.getcwd()
utils_dir = os.path.join(current_dir, '..', 'utils')
if os.path.exists(utils_dir):
    sys.path.insert(0, utils_dir)

# Import our modules
from config import Config
from gee_auth import initialize_earth_engine
from gee_data_extractor import GEEDataExtractor
from weather_api import WeatherAPI
from soil_data_collector import SoilDataCollector

class DataCollector:
    def __init__(self):
        """Initialize the data collection system"""
        self.config = Config()
        self.gee_extractor = None
        self.weather_api = None
        self.soil_collector = None
        
    def initialize_systems(self):
        """Initialize all data collection systems"""
        print("🔧 INITIALIZING ALL SYSTEMS")
        print("=" * 35)
        
        # Initialize Google Earth Engine
        print("1️⃣ Google Earth Engine...")
        gee_success = initialize_earth_engine()
        
        # Initialize Weather API
        print("\n2️⃣ Weather API System...")
        self.weather_api = WeatherAPI()
        test_weather = self.weather_api.get_weather_for_location(30.9010, 75.8573)
        weather_success = test_weather is not None
        print(f"   Weather API Status: {'✅ Working' if weather_success else '❌ Failed'}")
        
        # Initialize Soil Data Collector
        print("\n3️⃣ Soil Data Collection System...")
        self.soil_collector = SoilDataCollector()
        test_soil = self.soil_collector.get_soilgrids_data(30.9010, 75.8573)
        soil_success = test_soil is not None
        print(f"   Soil Data Status: {'✅ Working' if soil_success else '❌ Failed'}")
        
        # Initialize GEE Data Extractor
        print("\n4️⃣ Satellite Data Extractor...")
        self.gee_extractor = GEEDataExtractor()
        
        return gee_success and weather_success and soil_success
    
    def create_farm_plots(self, num_plots=50):
        """Create Punjab farm plot network"""
        print("\n🗺️ CREATING PUNJAB FARM PLOT NETWORK")
        print("=" * 42)
        
        farm_plots = self.gee_extractor.create_punjab_farm_plots(num_plots=num_plots)
        
        plots_df = pd.DataFrame([{
            'plot_id': plot['plot_id'],
            'latitude': plot['latitude'],
            'longitude': plot['longitude'],
            'district': plot['district']
        } for plot in farm_plots])
        
        print(f"✅ Created {len(plots_df)} farm plots across Punjab")
        return plots_df, farm_plots
    
    def collect_satellite_data(self, farm_plots, start_date='2024-06-01', end_date='2024-08-31'):
        """Collect satellite data for all plots"""
        print(f"\n🛰️ COLLECTING REAL SATELLITE DATA (SENTINEL-2)")
        print("=" * 52)
        
        satellite_data = []
        successful_extractions = 0
        
        for idx, plot in enumerate(farm_plots):
            plot_id = plot['plot_id']
            geometry = plot['geometry']
            
            print(f"🔄 Processing {idx+1}/{len(farm_plots)}: {plot_id}", end=" ... ")
            
            try:
                sat_data = self.gee_extractor.extract_ndvi_sentinel2(geometry, start_date, end_date)
                
                plot_data = {
                    'plot_id': plot_id,
                    'latitude': plot['latitude'],
                    'longitude': plot['longitude'],
                    'district': plot['district'],
                    **sat_data
                }
                
                satellite_data.append(plot_data)
                
                if sat_data['data_source'] == 'Sentinel2_Real':
                    successful_extractions += 1
                    print("✅ Real data")
                else:
                    print("⚠️ Synthetic")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:30]}...")
                satellite_data.append({
                    'plot_id': plot_id,
                    'latitude': plot['latitude'],
                    'longitude': plot['longitude'],
                    'district': plot['district'],
                    'ndvi_mean': np.nan,
                    'ndwi_mean': np.nan,
                    'data_source': 'Failed'
                })
        
        satellite_df = pd.DataFrame(satellite_data)
        print(f"\n📊 SATELLITE DATA COLLECTION RESULTS:")
        print(f"   ✅ Total processed: {len(satellite_data)}")
        print(f"   🛰️ Real Sentinel-2: {successful_extractions}")
        
        return satellite_df
    
    def collect_weather_data(self, plots_df):
        """Collect weather data for all plots"""
        print(f"\n🌤️ COLLECTING WEATHER DATA FOR ALL PLOTS")
        print("=" * 45)
        
        weather_df = self.weather_api.get_weather_for_multiple_locations(plots_df)
        
        print(f"\n📊 WEATHER DATA SUMMARY:")
        print(f"   🌡️ Temperature range: {weather_df['temperature'].min():.1f}°C to {weather_df['temperature'].max():.1f}°C")
        print(f"   💧 Humidity range: {weather_df['humidity'].min():.0f}% to {weather_df['humidity'].max():.0f}%")
        
        return weather_df
    
    def collect_soil_data(self, plots_df):
        """Collect soil data for all plots"""
        print(f"\n🌱 COLLECTING COMPREHENSIVE SOIL DATA")
        print("=" * 40)
        
        soil_df = self.soil_collector.collect_soil_data_for_plots(plots_df)
        
        print(f"\n📊 SOIL DATA SUMMARY:")
        print(f"   🧪 pH range: {soil_df['pH'].min():.1f} to {soil_df['pH'].max():.1f}")
        print(f"   🌿 Organic Carbon: {soil_df['organic_carbon'].min():.2f}% to {soil_df['organic_carbon'].max():.2f}%")
        
        return soil_df
    
    def generate_yield_data(self, plots_df, satellite_df, soil_df, weather_df):
        """Generate realistic crop yield data"""
        print(f"\n🌾 GENERATING REALISTIC CROP YIELD DATA")
        print("=" * 42)
        
        yield_data = []
        
        crop_base_yields = {
            'Wheat': 4200,
            'Rice': 5800, 
            'Cotton': 480
        }
        
        for _, row in plots_df.iterrows():
            plot_id = row['plot_id']
            
            # Get corresponding data
            sat_row = satellite_df[satellite_df['plot_id'] == plot_id].iloc[0]
            soil_row = soil_df[soil_df['plot_id'] == plot_id].iloc[0]
            weather_row = weather_df[weather_df['plot_id'] == plot_id].iloc[0]
            
            # Extract key factors
            ndvi = sat_row['ndvi_mean'] if pd.notna(sat_row['ndvi_mean']) else 0.6
            soil_health = soil_row['soil_health_status']
            temperature = weather_row['temperature']
            
            # Calculate influence factors
            ndvi_factor = max(0.5, min(1.5, (ndvi - 0.2) / 0.5))
            soil_factor = {'Good': 1.1, 'Medium': 1.0, 'Poor': 0.85}[soil_health]
            temp_factor = 1.0 if temperature < 35 else max(0.8, 1.0 - (temperature - 35) * 0.02)
            
            # Generate yields for 3 years and 3 crops
            for year in [2022, 2023, 2024]:
                for crop, base_yield in crop_base_yields.items():
                    year_factor = np.random.normal(1.0, 0.1)
                    
                    final_yield = (base_yield * 
                                  ndvi_factor * 
                                  soil_factor * 
                                  temp_factor * 
                                  year_factor)
                    
                    final_yield = max(base_yield * 0.4, final_yield)
                    
                    yield_data.append({
                        'plot_id': plot_id,
                        'year': year,
                        'crop_type': crop,
                        'yield_kg_per_hectare': round(final_yield, 1),
                        'sowing_date': f'{year}-{6 if crop == "Rice" else 11}-{np.random.randint(1,20):02d}',
                        'harvest_date': f'{year if crop == "Rice" else year+1}-{10 if crop == "Rice" else 4}-{np.random.randint(1,25):02d}'
                    })
        
        yield_df = pd.DataFrame(yield_data)
        print(f"\n📊 CROP YIELD DATA SUMMARY:")
        print(f"   📈 Total yield records: {len(yield_df):,}")
        
        return yield_df
    
    def save_all_data(self, plots_df, satellite_df, weather_df, soil_df, yield_df):
        """Save all collected data"""
        print(f"\n💾 SAVING ALL COLLECTED DATA")
        print("=" * 30)
        
        # Create directories
        os.makedirs('../data/raw', exist_ok=True)
        
        # Save all datasets
        plots_df.to_csv('../data/raw/punjab_farm_plots.csv', index=False)
        satellite_df.to_csv('../data/raw/punjab_satellite_data.csv', index=False)
        weather_df.to_csv('../data/raw/punjab_weather_data.csv', index=False)
        soil_df.to_csv('../data/raw/punjab_soil_data.csv', index=False)
        yield_df.to_csv('../data/raw/punjab_crop_yields.csv', index=False)
        
        print("✅ All datasets saved successfully!")
        
        return {
            'plots': len(plots_df),
            'satellite': len(satellite_df),
            'weather': len(weather_df),
            'soil': len(soil_df),
            'yield': len(yield_df)
        }
    
    def run_complete_collection(self, num_plots=50):
        """Run the complete data collection pipeline"""
        print("🌾 PUNJAB SMART CROP ADVISORY - COMPLETE DATA COLLECTION")
        print("=" * 65)
        print(f"📅 Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Initialize systems
        if not self.initialize_systems():
            print("❌ Failed to initialize systems")
            return None
        
        # Create farm plots
        plots_df, farm_plots = self.create_farm_plots(num_plots)
        
        # Collect all data
        satellite_df = self.collect_satellite_data(farm_plots)
        weather_df = self.collect_weather_data(plots_df)
        soil_df = self.collect_soil_data(plots_df)
        yield_df = self.generate_yield_data(plots_df, satellite_df, soil_df, weather_df)
        
        # Save all data
        summary = self.save_all_data(plots_df, satellite_df, weather_df, soil_df, yield_df)
        
        print(f"\n✅ DATA COLLECTION COMPLETE!")
        print(f"🎯 Ready for Feature Engineering and Model Training!")
        
        return summary

if __name__ == "__main__":
    collector = DataCollector()
    summary = collector.run_complete_collection(num_plots=50)
    if summary:
        print(f"📊 Collection Summary: {summary}")
