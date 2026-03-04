import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "ml", "models", "scaler.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "ml", "models", "imputer.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "ml", "models", "feature_columns.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
imputer = joblib.load(IMPUTER_PATH)
feature_columns = joblib.load(FEATURES_PATH)


def predict_from_input(input_data):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([input_data])

        # One-hot encode (same as training)
        df = pd.get_dummies(df)

        # Add missing columns
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0

        # Keep only training columns in correct order
        df = df[feature_columns]

        # Apply imputer
        df_imputed = imputer.transform(df)

        # Apply scaler
        df_scaled = scaler.transform(df_imputed)

        # Predict
        probability = model.predict_proba(df_scaled)[0][1]
        prediction = int(probability >= 0.5)

        return {
            "prediction": prediction,
            "risk_probability": round(probability * 100, 2)
        }

    except Exception as e:
        print("Prediction error:", e)
        return None