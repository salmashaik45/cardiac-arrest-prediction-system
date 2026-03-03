import os
import joblib
import pandas as pd

# --------------------------
# Paths
# --------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "ml", "models", "scaler.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "ml", "models", "feature_columns.pkl")

# --------------------------
# Load Model
# --------------------------

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(FEATURES_PATH)

# --------------------------
# Prediction Function
# --------------------------

def predict_from_input(input_data):

    # Create DataFrame from input
    df = pd.DataFrame([input_data])

    # One-hot encode (same as training)
    df = pd.get_dummies(df)

    # Add any missing columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Ensure correct column order
    df = df[feature_columns]

    # Scale features
    scaled = scaler.transform(df)

    # Predict
    probability = model.predict_proba(scaled)[0][1]
    prediction = int(probability >= 0.5)

    return {
        "prediction": prediction,
        "risk_probability": round(probability * 100, 2)
    }