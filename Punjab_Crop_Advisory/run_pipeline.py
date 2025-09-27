#!/usr/bin/env python3
"""
Punjab Crop Advisory System - Complete Pipeline Runner
This script runs the complete ML pipeline from data collection to model training
"""

import os
import sys
import argparse
from datetime import datetime

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def run_complete_pipeline():
    """Run the complete pipeline"""
    print("🌾 PUNJAB CROP ADVISORY - COMPLETE PIPELINE RUNNER")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        from pipeline import PunjabCropAdvisoryPipeline
        
        # Initialize pipeline
        pipeline = PunjabCropAdvisoryPipeline()
        
        # Run complete pipeline
        print("\n🚀 Starting complete pipeline...")
        success = pipeline.run_complete_pipeline(
            num_plots=30,  # Reduced for faster execution
            skip_data_collection=False,
            skip_feature_engineering=False
        )
        
        if success:
            print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print("✅ Your Punjab Crop Advisory system is ready!")
            print("🌐 You can now run the web application: python app.py")
            return True
        else:
            print("\n❌ Pipeline failed. Please check the error messages above.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Pipeline failed with error: {e}")
        return False

def run_quick_demo():
    """Run a quick demo with minimal data"""
    print("🌾 PUNJAB CROP ADVISORY - QUICK DEMO")
    print("=" * 40)
    
    try:
        from pipeline import PunjabCropAdvisoryPipeline
        
        pipeline = PunjabCropAdvisoryPipeline()
        
        print("\n🚀 Running quick demo with minimal data...")
        success = pipeline.run_complete_pipeline(
            num_plots=10,  # Minimal data for demo
            skip_data_collection=False,
            skip_feature_engineering=False
        )
        
        if success:
            print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("🌐 Start the web app: python app.py")
            return True
        else:
            print("\n❌ Demo failed.")
            return False
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def check_system():
    """Check system status"""
    print("🔍 SYSTEM STATUS CHECK")
    print("=" * 25)
    
    # Check Python version
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Check required directories
    directories = ['data/raw', 'data/processed', 'models', 'src']
    for dir_path in directories:
        exists = os.path.exists(dir_path)
        print(f"📁 {dir_path}: {'✅' if exists else '❌'}")
    
    # Check if model exists
    model_exists = os.path.exists('models/punjab_crop_yield_predictor_final.pkl')
    print(f"🤖 Trained Model: {'✅' if model_exists else '❌'}")
    
    # Check key Python packages
    packages = ['pandas', 'numpy', 'sklearn', 'matplotlib', 'flask']
    for package in packages:
        try:
            __import__(package)
            print(f"📦 {package}: ✅")
        except ImportError:
            print(f"📦 {package}: ❌")
    
    return model_exists

def main():
    parser = argparse.ArgumentParser(description='Punjab Crop Advisory System')
    parser.add_argument('action', choices=['full', 'demo', 'check', 'webapp'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'full':
        success = run_complete_pipeline()
        sys.exit(0 if success else 1)
        
    elif args.action == 'demo':
        success = run_quick_demo()
        sys.exit(0 if success else 1)
        
    elif args.action == 'check':
        check_system()
        sys.exit(0)
        
    elif args.action == 'webapp':
        print("🌐 Starting Web Application...")
        try:
            import subprocess
            subprocess.run([sys.executable, 'app.py'])
        except KeyboardInterrupt:
            print("\n👋 Web application stopped.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🌾 Punjab Crop Advisory System")
        print("=" * 35)
        print("Available commands:")
        print("  python run_pipeline.py full     - Run complete pipeline")
        print("  python run_pipeline.py demo     - Run quick demo")
        print("  python run_pipeline.py check    - Check system status")
        print("  python run_pipeline.py webapp   - Start web application")
        print()
        print("For web interface only:")
        print("  python app.py                   - Start Flask web app")
    else:
        main()
