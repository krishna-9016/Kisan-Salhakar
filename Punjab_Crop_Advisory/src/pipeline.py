# Punjab Crop Advisory - Complete Pipeline
# Main pipeline that connects data collection, feature engineering, and model training

import os
import sys
from datetime import datetime
import argparse

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from data_collection import DataCollector
from feature_engineering import FeatureEngineer
from model_training import ModelTrainer
from prediction import CropYieldPredictor

class PunjabCropAdvisoryPipeline:
    def __init__(self):
        """Initialize the complete pipeline"""
        self.data_collector = DataCollector()
        self.feature_engineer = FeatureEngineer()
        self.model_trainer = ModelTrainer()
        self.predictor = None
        
    def run_complete_pipeline(self, num_plots=50, skip_data_collection=False, skip_feature_engineering=False):
        """Run the complete pipeline from data collection to model training"""
        
        print("🌾 PUNJAB SMART CROP ADVISORY - COMPLETE PIPELINE")
        print("=" * 60)
        print(f"📅 Pipeline Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Goal: End-to-end ML pipeline for Punjab crop yield prediction")
        
        try:
            # Step 1: Data Collection
            if not skip_data_collection:
                print(f"\n{'='*60}")
                print("STEP 1: DATA COLLECTION")
                print(f"{'='*60}")
                
                collection_summary = self.data_collector.run_complete_collection(num_plots=num_plots)
                if not collection_summary:
                    print("❌ Data collection failed")
                    return False
                print(f"✅ Data collection completed: {collection_summary}")
            else:
                print("\n⏭️ Skipping data collection (using existing data)")
            
            # Step 2: Feature Engineering
            if not skip_feature_engineering:
                print(f"\n{'='*60}")
                print("STEP 2: FEATURE ENGINEERING")
                print(f"{'='*60}")
                
                engineering_result = self.feature_engineer.run_feature_engineering()
                if not engineering_result:
                    print("❌ Feature engineering failed")
                    return False
                engineered_df, metadata = engineering_result
                print(f"✅ Feature engineering completed: {metadata['total_features']} features")
            else:
                print("\n⏭️ Skipping feature engineering (using existing processed data)")
            
            # Step 3: Model Training
            print(f"\n{'='*60}")
            print("STEP 3: MODEL TRAINING")
            print(f"{'='*60}")
            
            model_package = self.model_trainer.run_training_pipeline()
            if not model_package:
                print("❌ Model training failed")
                return False
            
            print(f"✅ Model training completed")
            print(f"   Best Model: {model_package['model_name']}")
            print(f"   R² Score: {model_package['performance']['test_r2']:.3f}")
            print(f"   RMSE: {model_package['performance']['test_rmse']:.1f} kg/hectare")
            
            # Step 4: Model Testing
            print(f"\n{'='*60}")
            print("STEP 4: MODEL TESTING")
            print(f"{'='*60}")
            
            test_result = self.test_trained_model()
            if test_result:
                print("✅ Model testing completed successfully")
            else:
                print("⚠️ Model testing completed with warnings")
            
            print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print(f"📊 Summary:")
            print(f"   ✅ Data Collection: {'Completed' if not skip_data_collection else 'Skipped'}")
            print(f"   ✅ Feature Engineering: {'Completed' if not skip_feature_engineering else 'Skipped'}")
            print(f"   ✅ Model Training: Completed")
            print(f"   ✅ Model Testing: Completed")
            print(f"   🎯 Best Model: {model_package['model_name']}")
            print(f"   📈 Performance: R² = {model_package['performance']['test_r2']:.3f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Pipeline failed with error: {e}")
            return False
    
    def test_trained_model(self):
        """Test the trained model with sample predictions"""
        print("🔬 Testing trained model with sample scenarios...")
        
        # Initialize predictor
        self.predictor = CropYieldPredictor()
        
        if not self.predictor.model_package:
            print("❌ Failed to load trained model")
            return False
        
        # Test scenarios
        test_scenarios = [
            {
                'name': "High-yield Wheat (Ludhiana)",
                'data': {
                    'ndvi_mean': 0.75,
                    'ndwi_mean': 0.30,
                    'temperature': 18.5,
                    'humidity': 68.0,
                    'rainfall': 2.5,
                    'pH': 7.2,
                    'organic_carbon': 0.85,
                    'N_available': 240.0,
                    'P_available': 28.0,
                    'K_available': 320.0,
                    'crop_type': 'Wheat',
                    'crop_type_encoded': 0,
                    'district': 'Ludhiana'
                },
                'expected_range': (4000, 5500)
            },
            {
                'name': "Premium Rice (Amritsar)", 
                'data': {
                    'ndvi_mean': 0.82,
                    'ndwi_mean': 0.35,
                    'temperature': 28.0,
                    'humidity': 78.0,
                    'rainfall': 5.2,
                    'pH': 7.8,
                    'organic_carbon': 0.72,
                    'N_available': 180.0,
                    'P_available': 22.0,
                    'K_available': 290.0,
                    'crop_type': 'Rice',
                    'crop_type_encoded': 1,
                    'district': 'Amritsar'
                },
                'expected_range': (5000, 6500)
            },
            {
                'name': "Stressed Cotton (Bathinda)",
                'data': {
                    'ndvi_mean': 0.45,
                    'ndwi_mean': 0.12,
                    'temperature': 42.5,
                    'humidity': 35.0,
                    'rainfall': 0.8,
                    'pH': 8.5,
                    'organic_carbon': 0.42,
                    'N_available': 95.0,
                    'P_available': 12.0,
                    'K_available': 110.0,
                    'crop_type': 'Cotton',
                    'crop_type_encoded': 2,
                    'district': 'Bathinda'
                },
                'expected_range': (300, 500)
            }
        ]
        
        all_tests_passed = True
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🧪 Test {i}: {scenario['name']}")
            
            result = self.predictor.predict_yield(scenario['data'])
            
            if 'error' in result:
                print(f"   ❌ Prediction failed: {result['error']}")
                all_tests_passed = False
                continue
            
            predicted_yield = result['predicted_yield']
            expected_min, expected_max = scenario['expected_range']
            
            # Check if prediction is within expected range
            is_realistic = expected_min <= predicted_yield <= expected_max
            
            print(f"   Predicted Yield: {predicted_yield} kg/hectare")
            print(f"   Expected Range: {expected_min}-{expected_max} kg/hectare")
            print(f"   Category: {result['yield_category']}")
            print(f"   Status: {'✅ Realistic' if is_realistic else '⚠️ Outside expected range'}")
            print(f"   Recommendations: {len(result['recommendations'])} items")
            
            if not is_realistic:
                all_tests_passed = False
        
        # Model info
        model_info = self.predictor.get_model_info()
        print(f"\n📊 Model Information:")
        print(f"   Model: {model_info['model_name']}")
        print(f"   Training Date: {model_info['training_date']}")
        print(f"   Test R²: {model_info['performance']['test_r2']:.3f}")
        print(f"   Test RMSE: {model_info['performance']['test_rmse']:.1f} kg/ha")
        
        return all_tests_passed
    
    def run_prediction_only(self, input_data):
        """Run prediction only (for API usage)"""
        if not self.predictor:
            self.predictor = CropYieldPredictor()
        
        if not self.predictor.model_package:
            return {'error': 'Model not available'}
        
        return self.predictor.predict_yield(input_data)
    
    def get_pipeline_status(self):
        """Check the status of pipeline components"""
        status = {
            'data_files': {},
            'model_files': {},
            'pipeline_ready': True
        }
        
        # Check data files
        data_files = [
            '../data/raw/punjab_farm_plots.csv',
            '../data/raw/punjab_satellite_data.csv', 
            '../data/raw/punjab_weather_data.csv',
            '../data/raw/punjab_soil_data.csv',
            '../data/raw/punjab_crop_yields.csv',
            '../data/processed/master_dataset_final_engineered.csv'
        ]
        
        for file_path in data_files:
            file_name = os.path.basename(file_path)
            status['data_files'][file_name] = os.path.exists(file_path)
            if not os.path.exists(file_path):
                status['pipeline_ready'] = False
        
        # Check model files
        model_files = [
            '../models/punjab_crop_yield_predictor_final.pkl',
            '../models/model_performance_summary.json'
        ]
        
        for file_path in model_files:
            file_name = os.path.basename(file_path)
            status['model_files'][file_name] = os.path.exists(file_path)
            if not os.path.exists(file_path):
                status['pipeline_ready'] = False
        
        return status

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Punjab Crop Advisory Pipeline')
    parser.add_argument('--action', choices=['full', 'train', 'predict', 'status'], 
                       default='full', help='Action to perform')
    parser.add_argument('--num-plots', type=int, default=50, 
                       help='Number of farm plots to create')
    parser.add_argument('--skip-data', action='store_true', 
                       help='Skip data collection')
    parser.add_argument('--skip-features', action='store_true', 
                       help='Skip feature engineering')
    
    args = parser.parse_args()
    
    pipeline = PunjabCropAdvisoryPipeline()
    
    if args.action == 'full':
        # Run complete pipeline
        success = pipeline.run_complete_pipeline(
            num_plots=args.num_plots,
            skip_data_collection=args.skip_data,
            skip_feature_engineering=args.skip_features
        )
        sys.exit(0 if success else 1)
        
    elif args.action == 'train':
        # Run training only
        model_package = pipeline.model_trainer.run_training_pipeline()
        if model_package:
            print("✅ Training completed successfully")
            sys.exit(0)
        else:
            print("❌ Training failed")
            sys.exit(1)
            
    elif args.action == 'predict':
        # Test prediction
        test_result = pipeline.test_trained_model()
        sys.exit(0 if test_result else 1)
        
    elif args.action == 'status':
        # Check pipeline status
        status = pipeline.get_pipeline_status()
        print("📊 Pipeline Status:")
        print(f"   Pipeline Ready: {'✅' if status['pipeline_ready'] else '❌'}")
        print(f"   Data Files: {sum(status['data_files'].values())}/{len(status['data_files'])}")
        print(f"   Model Files: {sum(status['model_files'].values())}/{len(status['model_files'])}")
        
        for category, files in [('Data Files', status['data_files']), 
                               ('Model Files', status['model_files'])]:
            print(f"\n   {category}:")
            for file_name, exists in files.items():
                print(f"     {'✅' if exists else '❌'} {file_name}")
        
        sys.exit(0 if status['pipeline_ready'] else 1)

if __name__ == "__main__":
    main()
