# Punjab Crop Advisory - Model Training Module
# Converted from 03_Model_Training.ipynb

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import pickle
import joblib
import json

# Try to import XGBoost and LightGBM (optional)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

class ModelTrainer:
    def __init__(self):
        """Initialize the model training system"""
        self.models = {}
        self.trained_models = {}
        self.results = []
        self.best_model = None
        self.scaler = StandardScaler()
        
    def load_processed_data(self):
        """Load the feature-engineered dataset"""
        print("\n📂 LOADING PROCESSED DATASET")
        print("=" * 32)
        
        try:
            master_df = pd.read_csv('../data/processed/master_dataset_final_engineered.csv')
            
            print(f"✅ Dataset loaded successfully:")
            print(f"   📊 Shape: {master_df.shape[0]} rows × {master_df.shape[1]} columns")
            print(f"   🎯 Target: yield_kg_per_hectare")
            
            # Display basic statistics
            target_stats = master_df['yield_kg_per_hectare'].describe()
            print(f"\n📈 Target Variable Statistics:")
            print(f"   Mean: {target_stats['mean']:.1f} kg/ha")
            print(f"   Median: {target_stats['50%']:.1f} kg/ha")
            print(f"   Std: {target_stats['std']:.1f} kg/ha")
            print(f"   Range: {target_stats['min']:.1f} - {target_stats['max']:.1f} kg/ha")
            
            return master_df
            
        except FileNotFoundError:
            print("❌ Dataset not found. Please run feature engineering first")
            return None
    
    def prepare_ml_dataset(self, df):
        """Prepare dataset for machine learning"""
        print("\n🛠️ FEATURE SELECTION & DATA PREPARATION")
        print("=" * 42)
        
        print("🔄 Preparing dataset for ML training...")
        
        ml_df = df.copy()
        target_col = 'yield_kg_per_hectare'
        
        # Columns to exclude from features
        exclude_cols = [
            'plot_id', 'sowing_date', 'harvest_date', 
            target_col
        ]
        
        # Identify categorical columns that need encoding
        categorical_cols = []
        for col in ml_df.columns:
            if ml_df[col].dtype == 'object' and col not in exclude_cols:
                categorical_cols.append(col)
        
        print(f"📋 Found {len(categorical_cols)} categorical columns to encode: {categorical_cols}")
        
        # Encode categorical variables
        label_encoders = {}
        for col in categorical_cols:
            if col in ml_df.columns:
                le = LabelEncoder()
                ml_df[f'{col}_encoded'] = le.fit_transform(ml_df[col].astype(str))
                label_encoders[col] = le
                print(f"   ✅ Encoded {col}: {len(le.classes_)} unique values")
        
        # Select features for training
        feature_cols = []
        for col in ml_df.columns:
            if col not in exclude_cols and col not in categorical_cols:
                feature_cols.append(col)
        
        print(f"\n📊 Selected {len(feature_cols)} features for training")
        
        # Create feature matrix and target vector
        X = ml_df[feature_cols]
        y = ml_df[target_col]
        
        # Handle missing values
        print(f"🔧 Handling missing values...")
        missing_before = X.isnull().sum().sum()
        print(f"   Missing values before: {missing_before}")
        
        # Fill missing values
        for col in X.columns:
            if X[col].dtype in ['float64', 'int64']:
                X[col] = X[col].fillna(X[col].median())
            else:
                X[col] = X[col].fillna(X[col].mode()[0] if len(X[col].mode()) > 0 else 0)
        
        missing_after = X.isnull().sum().sum()
        print(f"   Missing values after: {missing_after}")
        
        print(f"\n✅ Dataset prepared: {len(X)} samples × {len(feature_cols)} features")
        
        return X, y, feature_cols, label_encoders
    
    def split_data(self, X, y, master_df):
        """Split data into train and test sets"""
        print(f"\n📊 TRAIN-TEST SPLIT STRATEGY")
        print("=" * 32)
        
        # Use stratified split based on crop type if available
        if 'crop_type' in master_df.columns:
            crop_types = master_df.loc[X.index, 'crop_type']
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=crop_types
            )
            print("✅ Using stratified split based on crop type")
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            print("✅ Using random split")
        
        print(f"\n📊 Split Results:")
        print(f"   Training samples: {len(X_train):,}")
        print(f"   Test samples: {len(X_test):,}")
        print(f"   Features: {X_train.shape[1]}")
        
        # Feature scaling
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"✅ Features scaled for linear models")
        
        return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled
    
    def setup_models(self):
        """Setup machine learning models"""
        self.models = {
            'Random Forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                subsample=0.8,
                random_state=42
            ),
            
            'Extra Trees': ExtraTreesRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            
            'Ridge Regression': Ridge(alpha=1.0),
            'Linear Regression': LinearRegression()
        }
        
        # Add XGBoost if available
        if XGBOOST_AVAILABLE:
            self.models['XGBoost'] = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1
            )
        
        # Add LightGBM if available
        if LIGHTGBM_AVAILABLE:
            self.models['LightGBM'] = lgb.LGBMRegressor(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
    
    def evaluate_model(self, model, X_train, X_test, y_train, y_test, model_name, use_scaling=False, X_train_scaled=None, X_test_scaled=None):
        """Train and evaluate a machine learning model"""
        print(f"\n🔄 Training {model_name}...")
        
        # Select appropriate data
        if use_scaling and X_train_scaled is not None:
            X_train_model = X_train_scaled
            X_test_model = X_test_scaled
        else:
            X_train_model = X_train
            X_test_model = X_test
        
        # Train the model
        model.fit(X_train_model, y_train)
        
        # Make predictions
        y_train_pred = model.predict(X_train_model)
        y_test_pred = model.predict(X_test_model)
        
        # Calculate metrics
        metrics = {
            'model_name': model_name,
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'model': model
        }
        
        # Cross-validation score
        try:
            cv_scores = cross_val_score(model, X_train_model, y_train, cv=5, scoring='r2')
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
        except:
            metrics['cv_r2_mean'] = np.nan
            metrics['cv_r2_std'] = np.nan
        
        print(f"   ✅ {model_name} - R² Score: {metrics['test_r2']:.3f}, RMSE: {metrics['test_rmse']:.1f}")
        
        return metrics
    
    def train_all_models(self, X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled):
        """Train and evaluate all models"""
        print(f"\n🏋️ COMPREHENSIVE MODEL TRAINING")
        print("=" * 35)
        
        self.setup_models()
        self.results = []
        self.trained_models = {}
        
        print("🚀 Starting model training pipeline...")
        
        for name, model in self.models.items():
            try:
                # Determine if scaling is needed
                use_scaling = name in ['Ridge Regression', 'Linear Regression', 'Lasso', 'ElasticNet']
                
                # Train and evaluate
                metrics = self.evaluate_model(
                    model, X_train, X_test, y_train, y_test, name, 
                    use_scaling, X_train_scaled, X_test_scaled
                )
                self.results.append(metrics)
                
                # Store model with scaling info
                self.trained_models[name] = {
                    'model': model,
                    'use_scaling': use_scaling,
                    'scaler': self.scaler if use_scaling else None
                }
                
            except Exception as e:
                print(f"   ❌ {name} failed: {e}")
        
        print(f"\n✅ Model training completed! {len(self.results)} models trained successfully.")
    
    def analyze_results(self):
        """Analyze and compare model results"""
        print(f"\n📊 MODEL PERFORMANCE COMPARISON")
        print("=" * 35)
        
        if not self.results:
            print("❌ No models trained successfully")
            return None
        
        # Create results DataFrame
        results_df = pd.DataFrame(self.results)
        results_df = results_df.sort_values('test_r2', ascending=False)
        
        print("🏆 Model Performance Ranking:")
        print("=" * 70)
        print(f"{'Rank':<4} {'Model':<20} {'Test R²':<10} {'Test RMSE':<12} {'Test MAE':<10} {'CV R²':<15}")
        print("-" * 70)
        
        for idx, (_, row) in enumerate(results_df.iterrows(), 1):
            cv_score = f"{row['cv_r2_mean']:.3f}±{row['cv_r2_std']:.3f}" if not np.isnan(row['cv_r2_mean']) else "N/A"
            print(f"{idx:<4} {row['model_name']:<20} "
                  f"{row['test_r2']:<10.3f} "
                  f"{row['test_rmse']:<12.1f} "
                  f"{row['test_mae']:<10.1f} "
                  f"{cv_score:<15}")
        
        # Get best model
        best_model_name = results_df.iloc[0]['model_name']
        best_model_r2 = results_df.iloc[0]['test_r2']
        best_model_rmse = results_df.iloc[0]['test_rmse']
        
        print(f"\n🥇 Best Model: {best_model_name}")
        print(f"   R² Score: {best_model_r2:.3f}")
        print(f"   RMSE: {best_model_rmse:.1f} kg/hectare")
        
        # Store best model
        self.best_model = {
            'name': best_model_name,
            'model': self.trained_models[best_model_name],
            'metrics': results_df.iloc[0].to_dict()
        }
        
        return results_df
    
    def create_visualizations(self, results_df, X_test, y_test):
        """Create performance visualizations"""
        print(f"\n📈 CREATING VISUALIZATIONS")
        print("=" * 30)
        
        # Create output directory
        os.makedirs('../data/processed', exist_ok=True)
        
        if results_df is not None and len(results_df) > 0:
            # Model comparison plot
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # R² Score comparison
            results_df.plot(x='model_name', y=['train_r2', 'test_r2'], kind='bar', ax=axes[0])
            axes[0].set_title('🎯 R² Score Comparison')
            axes[0].set_ylabel('R² Score')
            axes[0].legend(['Training R²', 'Test R²'])
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].set_ylim(0, 1)
            
            # RMSE comparison
            results_df.plot(x='model_name', y=['train_rmse', 'test_rmse'], kind='bar', ax=axes[1])
            axes[1].set_title('📊 RMSE Comparison (Lower = Better)')
            axes[1].set_ylabel('RMSE (kg/hectare)')
            axes[1].legend(['Training RMSE', 'Test RMSE'])
            axes[1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('../data/processed/model_performance_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✅ Performance comparison plots saved")
        
        # Prediction vs Actual plot for best model
        if self.best_model:
            best_model_obj = self.best_model['model']['model']
            use_scaling = self.best_model['model']['use_scaling']
            
            if use_scaling:
                X_test_model = self.scaler.transform(X_test)
            else:
                X_test_model = X_test
            
            y_pred = best_model_obj.predict(X_test_model)
            
            plt.figure(figsize=(10, 8))
            plt.scatter(y_test, y_pred, alpha=0.6, color='blue', s=50)
            plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            plt.xlabel('Actual Yield (kg/hectare)')
            plt.ylabel('Predicted Yield (kg/hectare)')
            plt.title(f'🎯 {self.best_model["name"]} - Prediction vs Actual')
            plt.grid(True, alpha=0.3)
            
            # Add R² score to plot
            r2 = self.best_model['metrics']['test_r2']
            plt.text(0.05, 0.95, f'R² = {r2:.3f}', transform=plt.gca().transAxes, 
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig('../data/processed/prediction_vs_actual_final.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✅ Prediction vs actual plot saved")
    
    def save_model(self, feature_names, encoders):
        """Save the best model and metadata"""
        print(f"\n💾 SAVING FINAL MODEL")
        print("=" * 20)
        
        if not self.best_model:
            print("❌ No best model to save")
            return None
        
        # Create models directory
        os.makedirs('../models', exist_ok=True)
        
        # Create comprehensive model package
        model_package = {
            'model': self.best_model['model']['model'],
            'model_name': self.best_model['name'],
            'feature_names': feature_names,
            'label_encoders': encoders,
            'scaler': self.best_model['model']['scaler'],
            'use_scaling': self.best_model['model']['use_scaling'],
            
            # Performance metrics
            'performance': {
                'train_r2': float(self.best_model['metrics']['train_r2']),
                'test_r2': float(self.best_model['metrics']['test_r2']),
                'train_mae': float(self.best_model['metrics']['train_mae']),
                'test_mae': float(self.best_model['metrics']['test_mae']),
                'train_rmse': float(self.best_model['metrics']['train_rmse']),
                'test_rmse': float(self.best_model['metrics']['test_rmse'])
            },
            
            # Training metadata
            'metadata': {
                'training_date': datetime.now().isoformat(),
                'target_variable': 'yield_kg_per_hectare'
            }
        }
        
        # Save the model
        model_filename = '../models/punjab_crop_yield_predictor_final.pkl'
        with open(model_filename, 'wb') as f:
            pickle.dump(model_package, f)
        
        print(f"✅ Final model saved: {model_filename}")
        
        # Also save as joblib
        joblib_filename = '../models/punjab_crop_yield_predictor_final.joblib'
        joblib.dump(model_package, joblib_filename)
        print(f"✅ Joblib version saved: {joblib_filename}")
        
        # Save performance summary
        performance_summary = {
            'final_model': str(self.best_model['name']),
            'performance_metrics': model_package['performance'],
            'training_summary': {
                'training_date': datetime.now().isoformat(),
                'target_variable': 'yield_kg_per_hectare'
            }
        }
        
        with open('../models/model_performance_summary.json', 'w') as f:
            json.dump(performance_summary, f, indent=2)
        
        print(f"✅ Performance summary saved")
        
        return model_package
    
    def run_training_pipeline(self):
        """Run the complete model training pipeline"""
        print("🤖 PUNJAB SMART CROP ADVISORY - MACHINE LEARNING MODEL TRAINING")
        print("=" * 70)
        print(f"📅 Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load processed data
        master_df = self.load_processed_data()
        if master_df is None:
            return None
        
        # Prepare ML dataset
        X, y, feature_names, encoders = self.prepare_ml_dataset(master_df)
        
        # Split data
        X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled = self.split_data(X, y, master_df)
        
        # Train all models
        self.train_all_models(X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled)
        
        # Analyze results
        results_df = self.analyze_results()
        
        # Create visualizations
        self.create_visualizations(results_df, X_test, y_test)
        
        # Save best model
        model_package = self.save_model(feature_names, encoders)
        
        print(f"\n✅ MODEL TRAINING PIPELINE COMPLETE!")
        print(f"🎯 Best Model: {self.best_model['name'] if self.best_model else 'None'}")
        
        return model_package

if __name__ == "__main__":
    trainer = ModelTrainer()
    model_package = trainer.run_training_pipeline()
    if model_package:
        print(f"🎉 Training completed successfully!")
        print(f"📊 Best model R² score: {model_package['performance']['test_r2']:.3f}")
