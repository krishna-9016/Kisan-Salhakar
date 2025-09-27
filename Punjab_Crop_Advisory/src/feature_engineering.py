# Punjab Crop Advisory - Feature Engineering Module
# Converted from 02_Feature_Engineering_EDA.ipynb

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    def __init__(self):
        """Initialize the feature engineering system"""
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_raw_data(self):
        """Load all collected datasets"""
        print("\n📂 LOADING ALL COLLECTED DATASETS")
        print("=" * 40)
        
        try:
            plots_df = pd.read_csv('../data/raw/punjab_farm_plots.csv')
            satellite_df = pd.read_csv('../data/raw/punjab_satellite_data.csv')
            weather_df = pd.read_csv('../data/raw/punjab_weather_data.csv')
            soil_df = pd.read_csv('../data/raw/punjab_soil_data.csv')
            yield_df = pd.read_csv('../data/raw/punjab_crop_yields.csv')
            
            print("✅ Datasets loaded successfully:")
            print(f"   📍 Farm Plots: {plots_df.shape[0]} plots × {plots_df.shape[1]} features")
            print(f"   🛰️ Satellite Data: {satellite_df.shape[0]} records × {satellite_df.shape[1]} features")
            print(f"   🌤️ Weather Data: {weather_df.shape[0]} records × {weather_df.shape[1]} features")
            print(f"   🌱 Soil Data: {soil_df.shape[0]} samples × {soil_df.shape[1]} features")
            print(f"   🌾 Yield Data: {yield_df.shape[0]} records × {yield_df.shape[1]} features")
            
            return plots_df, satellite_df, weather_df, soil_df, yield_df
            
        except FileNotFoundError as e:
            print(f"❌ Error loading datasets: {e}")
            return None, None, None, None, None
    
    def create_master_dataset(self, plots_df, satellite_df, weather_df, soil_df, yield_df):
        """Integrate all data sources into a comprehensive dataset"""
        print("\n🔗 DATA INTEGRATION - CREATING MASTER DATASET")
        print("=" * 48)
        
        print("🔄 Merging all datasets...")
        
        # Start with yield data as the base
        master_df = yield_df.copy()
        print(f"📊 Base dataset: {len(master_df)} yield records")
        
        # Add farm plot information
        master_df = master_df.merge(plots_df, on='plot_id', how='left')
        print(f"📍 Added plot locations: {len(master_df)} records")
        
        # Add satellite data
        satellite_cols = ['plot_id', 'ndvi_mean', 'ndwi_mean', 'blue', 'green', 'red', 'nir', 'data_source']
        available_sat_cols = [col for col in satellite_cols if col in satellite_df.columns]
        master_df = master_df.merge(satellite_df[available_sat_cols], on='plot_id', how='left', suffixes=('', '_sat'))
        print(f"🛰️ Added satellite data: {len(master_df)} records")
        
        # Add soil data
        soil_cols = [
            'plot_id', 'pH', 'organic_carbon', 'N_available', 'P_available', 'K_available',
            'soil_health_status', 'data_source'
        ]
        available_soil_cols = [col for col in soil_cols if col in soil_df.columns]
        master_df = master_df.merge(soil_df[available_soil_cols], on='plot_id', how='left', suffixes=('', '_soil'))
        print(f"🌱 Added soil data: {len(master_df)} records")
        
        # Add weather data
        weather_cols = ['plot_id', 'temperature', 'humidity', 'rainfall', 'wind_speed', 'data_source']
        available_weather_cols = [col for col in weather_cols if col in weather_df.columns]
        master_df = master_df.merge(weather_df[available_weather_cols], on='plot_id', how='left', suffixes=('', '_weather'))
        print(f"🌤️ Added weather data: {len(master_df)} records")
        
        print(f"\n✅ MASTER DATASET CREATED!")
        print(f"📊 Final Shape: {master_df.shape[0]} rows × {master_df.shape[1]} columns")
        
        return master_df
    
    def engineer_advanced_features(self, df):
        """Create sophisticated agricultural features for ML"""
        print(f"\n🛠️ ADVANCED FEATURE ENGINEERING")
        print("=" * 35)
        
        df = df.copy()
        print("Creating advanced agricultural features...")
        
        # 1. Vegetation Health Composite Index
        if 'ndvi_mean' in df.columns and 'ndwi_mean' in df.columns:
            df['vegetation_health_score'] = (
                df['ndvi_mean'].fillna(0.6) * 0.7 + 
                df['ndwi_mean'].fillna(0.3) * 0.3
            )
            print("   ✅ Vegetation Health Score")
        
        # 2. Soil Fertility Index
        if all(col in df.columns for col in ['organic_carbon', 'N_available', 'P_available']):
            df['soil_fertility_index'] = (
                (df['organic_carbon'].fillna(0.5) / 1.0) * 0.4 +
                (df['N_available'].fillna(180) / 300) * 0.3 +
                (df['P_available'].fillna(15) / 30) * 0.3
            ).clip(0, 1)
            print("   ✅ Soil Fertility Index")
        
        # 3. Climate Stress Indicators
        if 'temperature' in df.columns:
            df['heat_stress'] = np.maximum(0, df['temperature'].fillna(25) - 35) / 10
            df['cold_stress'] = np.maximum(0, 10 - df['temperature'].fillna(25)) / 10
            print("   ✅ Temperature Stress Indicators")
        
        if 'humidity' in df.columns and 'rainfall' in df.columns:
            df['drought_risk'] = np.where(
                (df['rainfall'].fillna(0) < 1) & (df['humidity'].fillna(70) < 40),
                1 - (df['humidity'].fillna(70) / 100),
                0
            )
            print("   ✅ Drought Risk Indicator")
        
        # 4. Nutrient Balance Ratios
        if all(col in df.columns for col in ['N_available', 'P_available', 'K_available']):
            df['N_P_ratio'] = df['N_available'].fillna(180) / (df['P_available'].fillna(15) + 1)
            df['N_K_ratio'] = df['N_available'].fillna(180) / (df['K_available'].fillna(250) + 1)
            df['P_K_ratio'] = df['P_available'].fillna(15) / (df['K_available'].fillna(250) + 1)
            print("   ✅ Nutrient Balance Ratios")
        
        # 5. Temporal Features
        if 'sowing_date' in df.columns:
            df['sowing_date'] = pd.to_datetime(df['sowing_date'], errors='coerce')
            df['sowing_month'] = df['sowing_date'].dt.month
            df['sowing_day_of_year'] = df['sowing_date'].dt.dayofyear
            
            # Crop season indicators
            df['is_kharif'] = df['sowing_month'].between(6, 9).astype(int)
            df['is_rabi'] = (df['sowing_month'].between(10, 12) | df['sowing_month'].between(1, 3)).astype(int)
            print("   ✅ Seasonal Features")
        
        # 6. Soil pH Categories
        if 'pH' in df.columns:
            df['soil_pH_category'] = pd.cut(
                df['pH'].fillna(7.5),
                bins=[0, 6.5, 7.5, 8.5, 14],
                labels=['Acidic', 'Neutral', 'Slightly_Alkaline', 'Highly_Alkaline']
            )
            print("   ✅ Soil pH Categories")
        
        # 7. Comprehensive Yield Potential Score
        health_score = df.get('vegetation_health_score', 0.6)
        fertility_score = df.get('soil_fertility_index', 0.7)
        climate_score = 1 - (df.get('heat_stress', 0) + df.get('drought_risk', 0))
        
        df['yield_potential_score'] = (
            health_score * 0.35 +
            fertility_score * 0.40 +
            climate_score * 0.25
        ).clip(0, 1)
        print("   ✅ Comprehensive Yield Potential Score")
        
        return df
    
    def create_visualizations(self, df):
        """Create comprehensive visualizations"""
        print(f"\n📈 CREATING VISUALIZATIONS")
        print("=" * 30)
        
        # Create output directory
        os.makedirs('../data/processed', exist_ok=True)
        
        # Distribution analysis
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('🌾 Punjab Crop Advisory - Key Variable Distributions', fontsize=16, fontweight='bold')
        
        # 1. Yield Distribution by Crop
        if 'crop_type' in df.columns:
            sns.boxplot(data=df, x='crop_type', y='yield_kg_per_hectare', ax=axes[0,0])
            axes[0,0].set_title('🌾 Yield Distribution by Crop Type')
            axes[0,0].set_ylabel('Yield (kg/hectare)')
            axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Vegetation Health Score Distribution
        if 'vegetation_health_score' in df.columns:
            sns.histplot(data=df, x='vegetation_health_score', bins=25, kde=True, ax=axes[0,1])
            axes[0,1].set_title('🌱 Vegetation Health Score Distribution')
            axes[0,1].set_xlabel('Vegetation Health Score')
        
        # 3. Soil Fertility vs Yield
        if 'soil_fertility_index' in df.columns:
            sns.scatterplot(data=df, x='soil_fertility_index', y='yield_kg_per_hectare', 
                            hue='crop_type', alpha=0.7, ax=axes[0,2])
            axes[0,2].set_title('🌱 Soil Fertility vs Yield')
            axes[0,2].set_xlabel('Soil Fertility Index')
        
        # Additional plots
        if 'temperature' in df.columns and 'district' in df.columns:
            sns.boxplot(data=df, x='district', y='temperature', ax=axes[1,0])
            axes[1,0].set_title('🌡️ Temperature by District')
            axes[1,0].tick_params(axis='x', rotation=45)
        
        if 'ndvi_mean' in df.columns:
            sns.scatterplot(data=df, x='ndvi_mean', y='yield_kg_per_hectare', 
                            hue='crop_type', alpha=0.6, ax=axes[1,1])
            axes[1,1].set_title('🛰️ NDVI vs Yield')
            axes[1,1].set_xlabel('NDVI (Vegetation Health)')
        
        if 'yield_potential_score' in df.columns:
            sns.histplot(data=df, x='yield_potential_score', bins=25, kde=True, ax=axes[1,2])
            axes[1,2].set_title('🎯 Yield Potential Score Distribution')
            axes[1,2].set_xlabel('Yield Potential Score (0-1)')
        
        plt.tight_layout()
        plt.savefig('../data/processed/eda_comprehensive_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Correlation analysis
        numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = ['plot_id', 'year', 'latitude', 'longitude', 'sowing_month']
        numeric_features = [col for col in numeric_features if col not in exclude_cols]
        
        if len(numeric_features) > 1 and 'yield_kg_per_hectare' in numeric_features:
            correlation_matrix = df[numeric_features].corr()
            yield_correlations = correlation_matrix['yield_kg_per_hectare'].sort_values(key=abs, ascending=False)
            
            # Create correlation heatmap
            plt.figure(figsize=(16, 12))
            top_features = yield_correlations.head(16).index.tolist()
            if len(top_features) > 1:
                selected_corr = correlation_matrix.loc[top_features, top_features]
                mask = np.triu(np.ones_like(selected_corr, dtype=bool))
                sns.heatmap(
                    selected_corr, 
                    annot=True, 
                    cmap='RdYlBu_r', 
                    center=0, 
                    square=True,
                    fmt='.2f',
                    cbar_kws={'shrink': 0.8},
                    mask=mask
                )
                plt.title('🔗 Feature Correlation Matrix (Top Features)', fontsize=16, fontweight='bold', pad=20)
                plt.tight_layout()
                plt.savefig('../data/processed/correlation_heatmap.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        print("✅ Visualizations created and saved")
    
    def save_engineered_data(self, df):
        """Save the engineered dataset and metadata"""
        print(f"\n💾 SAVING ENGINEERED DATASET")
        print("=" * 30)
        
        # Save the dataset
        df.to_csv('../data/processed/master_dataset_final_engineered.csv', index=False)
        
        # Create metadata
        metadata = {
            'creation_date': datetime.now().isoformat(),
            'total_records': int(len(df)),
            'total_features': int(df.shape[1]),
            'target_variable': 'yield_kg_per_hectare',
            'crops_analyzed': [str(crop) for crop in df['crop_type'].unique()] if 'crop_type' in df.columns else [],
            'districts_covered': [str(district) for district in df['district'].unique()] if 'district' in df.columns else [],
            'years_covered': [int(year) for year in sorted(df['year'].unique())] if 'year' in df.columns else []
        }
        
        import json
        with open('../data/processed/feature_engineering_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Engineered dataset and metadata saved")
        return metadata
    
    def run_feature_engineering(self):
        """Run the complete feature engineering pipeline"""
        print("📊 PUNJAB SMART CROP ADVISORY - FEATURE ENGINEERING & EDA")
        print("=" * 65)
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load raw data
        plots_df, satellite_df, weather_df, soil_df, yield_df = self.load_raw_data()
        
        if plots_df is None:
            print("❌ Failed to load raw data")
            return None
        
        # Create master dataset
        master_df = self.create_master_dataset(plots_df, satellite_df, weather_df, soil_df, yield_df)
        
        # Engineer features
        engineered_df = self.engineer_advanced_features(master_df)
        
        # Create visualizations
        self.create_visualizations(engineered_df)
        
        # Save engineered data
        metadata = self.save_engineered_data(engineered_df)
        
        print(f"\n✅ FEATURE ENGINEERING COMPLETE!")
        print(f"🎯 Dataset ready for ML training: {engineered_df.shape[0]} samples × {engineered_df.shape[1]} features")
        
        return engineered_df, metadata

if __name__ == "__main__":
    engineer = FeatureEngineer()
    result = engineer.run_feature_engineering()
    if result:
        engineered_df, metadata = result
        print(f"📊 Feature Engineering Summary: {metadata}")
