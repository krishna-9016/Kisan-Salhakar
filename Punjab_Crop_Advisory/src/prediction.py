# Punjab Crop Advisory - Prediction Module
# Production-ready prediction functions

import pickle
import numpy as np
import pandas as pd
import os
from datetime import datetime

class CropYieldPredictor:
    def __init__(self, model_path='../models/punjab_crop_yield_predictor_final.pkl'):
        """Initialize the predictor with trained model"""
        self.model_path = model_path
        self.model_package = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model package"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model_package = pickle.load(f)
            print(f"✅ Model loaded: {self.model_package['model_name']}")
            return True
        except FileNotFoundError:
            print(f"❌ Model file not found at: {self.model_path}")
            return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def engineer_features(self, input_data):
        """Engineer features from raw input data"""
        
        # Calculate vegetation health score
        ndvi = input_data.get('ndvi_mean', 0.6)
        ndwi = input_data.get('ndwi_mean', 0.3)
        vegetation_health_score = ndvi * 0.7 + ndwi * 0.3
        
        # Calculate soil fertility index
        oc = input_data.get('organic_carbon', 0.5)
        n_avail = input_data.get('N_available', 180)
        p_avail = input_data.get('P_available', 15)
        soil_fertility_index = (oc/1.0 * 0.4 + n_avail/300 * 0.3 + p_avail/30 * 0.3)
        
        # Calculate stress factors
        temp = input_data.get('temperature', 25)
        heat_stress = max(0, (temp - 35) / 10)
        cold_stress = max(0, (10 - temp) / 10)
        
        rainfall = input_data.get('rainfall', 0)
        humidity = input_data.get('humidity', 70)
        drought_risk = 1 - (humidity/100) if rainfall < 1 and humidity < 40 else 0
        
        # Calculate nutrient ratios
        k_avail = input_data.get('K_available', 250)
        n_p_ratio = n_avail / (p_avail + 1)
        n_k_ratio = n_avail / (k_avail + 1)
        p_k_ratio = p_avail / (k_avail + 1)
        
        # Calculate overall yield potential
        yield_potential_score = (
            vegetation_health_score * 0.35 +
            soil_fertility_index * 0.40 +
            (1 - heat_stress - drought_risk) * 0.25
        )
        
        # Seasonal features
        crop_type_encoded = input_data.get('crop_type_encoded', 0)
        is_kharif = 1 if crop_type_encoded in [1, 2] else 0  # Rice=1, Cotton=2
        is_rabi = 1 - is_kharif
        
        # Return engineered features
        engineered = {
            **input_data,
            'vegetation_health_score': vegetation_health_score,
            'soil_fertility_index': soil_fertility_index,
            'heat_stress': heat_stress,
            'cold_stress': cold_stress,
            'drought_risk': drought_risk,
            'yield_potential_score': yield_potential_score,
            'N_P_ratio': n_p_ratio,
            'N_K_ratio': n_k_ratio,
            'P_K_ratio': p_k_ratio,
            'is_kharif': is_kharif,
            'is_rabi': is_rabi
        }
        
        return engineered
    
    def predict_yield(self, input_data):
        """
        Predict crop yield using trained model
        
        Parameters:
        -----------
        input_data : dict
            Dictionary containing feature values
        
        Returns:
        --------
        dict
            Prediction results with confidence intervals
        """
        if not self.model_package:
            return {'error': 'Model not loaded'}
        
        try:
            model = self.model_package['model']
            feature_names = self.model_package['feature_names']
            encoders = self.model_package['label_encoders']
            scaler = self.model_package['scaler']
            use_scaling = self.model_package['use_scaling']
            
            # Engineer features
            complete_input = self.engineer_features(input_data)
            
            # Prepare input features in correct order
            features = []
            missing_features = []
            
            for feature in feature_names:
                if feature.endswith('_encoded'):
                    # Handle encoded categorical features
                    original_col = feature.replace('_encoded', '')
                    if original_col in encoders and original_col in complete_input:
                        try:
                            encoded_val = encoders[original_col].transform([str(complete_input[original_col])])[0]
                        except:
                            encoded_val = 0  # Default for unknown categories
                        features.append(encoded_val)
                    else:
                        features.append(0)  # Default value
                        missing_features.append(feature)
                else:
                    # Handle numeric features
                    if feature in complete_input:
                        features.append(complete_input[feature])
                    else:
                        features.append(0)  # Default value
                        missing_features.append(feature)
            
            # Convert to numpy array
            features_array = np.array(features).reshape(1, -1)
            
            # Apply scaling if needed
            if use_scaling and scaler is not None:
                features_array = scaler.transform(features_array)
            
            # Make prediction
            prediction = model.predict(features_array)[0]
            
            # Calculate prediction interval (approximate)
            if hasattr(model, 'estimators_'):
                # For ensemble methods, get prediction from all estimators
                predictions = [estimator.predict(features_array)[0] for estimator in model.estimators_]
                prediction_std = np.std(predictions)
                lower_bound = prediction - 1.96 * prediction_std
                upper_bound = prediction + 1.96 * prediction_std
            else:
                # Simple confidence interval
                prediction_std = prediction * 0.1  # Assume 10% uncertainty
                lower_bound = prediction - 1.96 * prediction_std
                upper_bound = prediction + 1.96 * prediction_std
            
            # Determine yield category
            crop_type = input_data.get('crop_type', 'Unknown')
            yield_category = self._categorize_yield(prediction, crop_type)
            
            return {
                'predicted_yield': round(prediction, 1),
                'lower_bound': round(max(0, lower_bound), 1),
                'upper_bound': round(upper_bound, 1),
                'confidence_interval': '95%',
                'yield_category': yield_category,
                'model_used': self.model_package['model_name'],
                'engineered_features': {
                    'vegetation_health_score': round(complete_input['vegetation_health_score'], 3),
                    'soil_fertility_index': round(complete_input['soil_fertility_index'], 3),
                    'yield_potential_score': round(complete_input['yield_potential_score'], 3),
                    'heat_stress': round(complete_input['heat_stress'], 3),
                    'drought_risk': round(complete_input['drought_risk'], 3)
                },
                'recommendations': self._get_recommendations(complete_input, crop_type),
                'missing_features_count': len(missing_features)
            }
            
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _categorize_yield(self, yield_val, crop_type):
        """Categorize yield as High, Medium, or Low"""
        if crop_type.lower() == 'wheat':
            if yield_val >= 4500:
                return 'High'
            elif yield_val >= 3500:
                return 'Medium'
            else:
                return 'Low'
        elif crop_type.lower() == 'rice':
            if yield_val >= 6000:
                return 'High'
            elif yield_val >= 5000:
                return 'Medium'
            else:
                return 'Low'
        elif crop_type.lower() == 'cotton':
            if yield_val >= 500:
                return 'High'
            elif yield_val >= 350:
                return 'Medium'
            else:
                return 'Low'
        else:
            return 'Unknown'
    
    def _get_recommendations(self, features, crop_type):
        """Generate recommendations based on feature analysis"""
        recommendations = []
        
        # Heat stress recommendations
        if features['heat_stress'] > 0.2:
            recommendations.append("High heat stress detected - consider heat-resistant varieties and adequate irrigation")
        
        # Drought risk recommendations
        if features['drought_risk'] > 0.2:
            recommendations.append("Drought risk present - ensure adequate irrigation and water management")
        
        # Soil fertility recommendations
        if features['soil_fertility_index'] < 0.5:
            recommendations.append("Low soil fertility - consider applying balanced fertilizers (NPK)")
        
        # Vegetation health recommendations
        if features['vegetation_health_score'] < 0.4:
            recommendations.append("Poor vegetation health - check plant nutrition and pest management")
        
        # Nutrient balance recommendations
        if features['N_P_ratio'] > 15:
            recommendations.append("High N:P ratio - consider phosphorus supplementation")
        elif features['N_P_ratio'] < 5:
            recommendations.append("Low N:P ratio - consider nitrogen supplementation")
        
        # pH recommendations
        pH = features.get('pH', 7.0)
        if pH < 6.5:
            recommendations.append("Acidic soil - consider lime application to improve pH")
        elif pH > 8.5:
            recommendations.append("Highly alkaline soil - consider gypsum application")
        
        # Crop-specific recommendations
        if crop_type.lower() == 'wheat' and features['temperature'] > 25:
            recommendations.append("Temperature stress for wheat - consider early sowing next season")
        elif crop_type.lower() == 'rice' and features.get('rainfall', 0) < 2:
            recommendations.append("Insufficient water for rice - ensure adequate irrigation")
        elif crop_type.lower() == 'cotton' and features['temperature'] < 20:
            recommendations.append("Temperature too low for cotton - ensure proper timing")
        
        # General recommendations if no specific issues
        if not recommendations:
            if features['yield_potential_score'] > 0.7:
                recommendations.append("Excellent growing conditions - maintain current practices")
            else:
                recommendations.append("Good conditions overall - minor optimizations can improve yield")
        
        return recommendations
    
    def predict_multiple_scenarios(self, scenarios_list):
        """Predict yield for multiple scenarios"""
        results = []
        
        for i, scenario in enumerate(scenarios_list):
            result = self.predict_yield(scenario)
            result['scenario_id'] = i + 1
            result['scenario_name'] = scenario.get('name', f'Scenario {i+1}')
            results.append(result)
        
        return results
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.model_package:
            return {'error': 'Model not loaded'}
        
        return {
            'model_name': self.model_package['model_name'],
            'training_date': self.model_package['metadata']['training_date'],
            'performance': self.model_package['performance'],
            'feature_count': len(self.model_package['feature_names']),
            'target_variable': self.model_package['metadata']['target_variable']
        }

# Convenience function for quick predictions
def predict_crop_yield(input_data, model_path='../models/punjab_crop_yield_predictor_final.pkl'):
    """
    Quick prediction function
    
    Parameters:
    -----------
    input_data : dict
        Dictionary containing feature values
    model_path : str
        Path to the saved model file
    
    Returns:
    --------
    dict
        Prediction results
    """
    predictor = CropYieldPredictor(model_path)
    return predictor.predict_yield(input_data)

# Example usage and testing
if __name__ == "__main__":
    # Test the predictor
    predictor = CropYieldPredictor()
    
    if predictor.model_package:
        # Test prediction with sample data
        test_input = {
            'ndvi_mean': 0.75,
            'ndwi_mean': 0.30,
            'temperature': 20.0,
            'humidity': 65.0,
            'rainfall': 2.0,
            'pH': 7.2,
            'organic_carbon': 0.80,
            'N_available': 220.0,
            'P_available': 25.0,
            'K_available': 300.0,
            'crop_type': 'Wheat',
            'crop_type_encoded': 0,
            'district': 'Ludhiana'
        }
        
        print("🌾 Testing prediction system...")
        result = predictor.predict_yield(test_input)
        
        if 'error' not in result:
            print(f"✅ Prediction successful!")
            print(f"   Predicted Yield: {result['predicted_yield']} kg/hectare")
            print(f"   Category: {result['yield_category']}")
            print(f"   Confidence Range: {result['lower_bound']} - {result['upper_bound']} kg/ha")
            print(f"   Recommendations: {len(result['recommendations'])} items")
        else:
            print(f"❌ Prediction failed: {result['error']}")
    else:
        print("❌ Model not loaded - please train the model first")
