import ee
import pandas as pd
import numpy as np
from datetime import datetime

class GEEDataExtractor:
    """Google Earth Engine data extraction for Punjab crops"""
    
    def __init__(self):
        self.initialized = False
        try:
            # Check if EE is already initialized
            ee.Number(1).getInfo()
            self.initialized = True
            print("✅ GEE already initialized")
        except:
            print("⚠️ GEE not initialized. Call initialize_earth_engine() first")
    
    def create_punjab_farm_plots(self, num_plots=50):
        """Create realistic farm plot locations across Punjab"""
        
        np.random.seed(42)
        
        # Punjab district coordinates (approximate centers)
        punjab_districts = {
            'Ludhiana': (30.901, 75.857),
            'Amritsar': (31.634, 74.872),
            'Jalandhar': (31.326, 75.576),
            'Bathinda': (30.211, 74.946),
            'Patiala': (30.341, 76.384),
            'Mohali': (30.704, 76.718),
            'Gurdaspur': (32.044, 75.407),
            'Kapurthala': (31.378, 75.381)
        }
        
        plots = []
        
        for i in range(1, num_plots + 1):
            # Select random district
            district = np.random.choice(list(punjab_districts.keys()))
            center_lat, center_lon = punjab_districts[district]
            
            # Add random offset within ~25km radius
            lat_offset = np.random.normal(0, 0.15)
            lon_offset = np.random.normal(0, 0.15)
            
            lat = center_lat + lat_offset
            lon = center_lon + lon_offset
            
            plots.append({
                'plot_id': f'PB_{i:03d}',
                'latitude': lat,
                'longitude': lon,
                'district': district,
                'geometry': ee.Geometry.Point([lon, lat])
            })
        
        print(f"✅ Created {len(plots)} farm plots across Punjab districts")
        return plots
    
    def extract_ndvi_sentinel2(self, geometry, start_date, end_date):
        """Extract NDVI from Sentinel-2 for a specific plot"""
        
        if not self.initialized:
            return self._generate_synthetic_satellite_data()
        
        def add_indices(image):
            # Calculate NDVI: (NIR - Red) / (NIR + Red)
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            # Calculate NDWI: (Green - NIR) / (Green + NIR)  
            ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
            return image.addBands([ndvi, ndwi])
        
        try:
            # Load Sentinel-2 collection
            collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                         .filterDate(start_date, end_date)
                         .filterBounds(geometry)
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                         .map(add_indices))
            
            # Get median composite
            median_image = collection.median()
            
            # Sample the point
            sample = median_image.sample(
                region=geometry.buffer(50),  # 50m buffer
                scale=10,  # 10m resolution
                numPixels=1
            ).first().getInfo()
            
            properties = sample['properties']
            
            return {
                'ndvi_mean': properties.get('NDVI', np.nan),
                'ndwi_mean': properties.get('NDWI', np.nan),
                'blue': properties.get('B2', np.nan),
                'green': properties.get('B3', np.nan),
                'red': properties.get('B4', np.nan),
                'nir': properties.get('B8', np.nan),
                'image_count': collection.size().getInfo(),
                'data_source': 'Sentinel2_Real'
            }
            
        except Exception as e:
            print(f"Sentinel-2 extraction error: {e}, using synthetic data")
            return self._generate_synthetic_satellite_data()
    
    def _generate_synthetic_satellite_data(self):
        """Generate realistic synthetic satellite data as fallback"""
        
        np.random.seed(42)
        
        return {
            'ndvi_mean': np.random.normal(0.65, 0.15),  # Healthy crop NDVI
            'ndwi_mean': np.random.normal(0.25, 0.1),   # Water content
            'blue': np.random.normal(0.08, 0.02),
            'green': np.random.normal(0.10, 0.02),
            'red': np.random.normal(0.06, 0.01),
            'nir': np.random.normal(0.35, 0.05),
            'image_count': np.random.randint(3, 12),
            'data_source': 'Synthetic_Fallback'
        }

# Global instance
gee_extractor = GEEDataExtractor()
if __name__ == "__main__":
    # Example usage
    from gee_auth import initialize_earth_engine
    
    if initialize_earth_engine():
        gee_extractor = GEEDataExtractor()
        plots = gee_extractor.create_punjab_farm_plots(10)
        
        for plot in plots:
            data = gee_extractor.extract_ndvi_sentinel2(
                geometry=plot['geometry'],
                start_date='2023-01-01',
                end_date='2023-12-31'
            )
            print(f"Plot {plot['plot_id']} ({plot['district']}): {data}")
    else:
        print("GEE initialization failed. Cannot extract data.")