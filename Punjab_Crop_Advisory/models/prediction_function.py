
def predict_crop_yield(input_data, model_path='../models/punjab_crop_yield_predictor_final.pkl'):
    """
    Predict crop yield using trained model

    Parameters:
    -----------
    input_data : dict
        Dictionary containing feature values
    model_path : str
        Path to the saved model file

    Returns:
    --------
    dict
        Prediction results with confidence intervals
    """
    import pickle
    import numpy as np
    import pandas as pd

    # Load model package
    with open(model_path, 'rb') as f:
        model_pkg = pickle.load(f)

    model = model_pkg['model']
    feature_names = model_pkg['feature_names']
    encoders = model_pkg['label_encoders']
    scaler = model_pkg['scaler']
    use_scaling = model_pkg['use_scaling']

    # Prepare input features
    features = []

    for feature in feature_names:
        if feature.endswith('_encoded'):
            # Handle encoded categorical features
            original_col = feature.replace('_encoded', '')
            if original_col in encoders and original_col in input_data:
                try:
                    encoded_val = encoders[original_col].transform([input_data[original_col]])[0]
                except:
                    encoded_val = 0  # Default for unknown categories
                features.append(encoded_val)
            else:
                features.append(0)  # Default value
        else:
            # Handle numeric features
            features.append(input_data.get(feature, 0))

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

    return {
        'predicted_yield': round(prediction, 1),
        'lower_bound': round(max(0, lower_bound), 1),
        'upper_bound': round(upper_bound, 1),
        'confidence_interval': '95%',
        'model_used': model_pkg['model_name']
    }
