import os
import joblib
import pandas as pd
import requests

# ------------------------------
# Model Loading
# ------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "ml", "models", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ------------------------------
# Default Values
# ------------------------------

DEFAULTS = {
    "age": 40,
    "sex": 1,
    "cholesterol": 190,
    "heart_rate": 80,
    "diabetes": 0,
    "family": 0,
    "smoke": 0,
    "alcohol": 0,
    "body_temp": 36.8,
    "prev_heart": 0,
    "meds": 0,
    "stress": 5,
    "activity": 3,
    "sleep": 7,
    "spo2": 95,
    "sbp": 120,
    "dbp": 80,
}

# ------------------------------
# Model Feature Order
# ------------------------------

MODEL_COLUMNS = [
    "Age",
    "Sex",
    "Cholesterol",
    "Heart Rate",
    "Diabetes",
    "Family History",
    "Smoking",
    "Alcohol Consumption",
    "Body Temperature",
    "Previous Heart Problems",
    "Medication Use",
    "Stress Level",
    "Physical Activity Days Per Week",
    "Sleep Hours Per Day",
    "Oxygen Saturation",
    "Systolic_BP",
    "Diastolic_BP",
]

# ------------------------------
# Sensor Data Fetch
# ------------------------------

def get_sensor_data():
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    api_key = os.getenv("THINGSPEAK_API_KEY")

    if not channel_id or not api_key:
        return {
            "heart_rate": DEFAULTS["heart_rate"],
            "spo2": DEFAULTS["spo2"],
            "body_temp": DEFAULTS["body_temp"],
        }

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {"api_key": api_key, "results": 1}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        feed = data["feeds"][0]

        heart_rate = float(feed["field1"])
        spo2 = float(feed["field2"])
        body_temp = float(feed["field3"])

        # Validate unrealistic values
        if heart_rate <= 0:
            heart_rate = DEFAULTS["heart_rate"]

        if spo2 <= 0:
            spo2 = DEFAULTS["spo2"]

        if body_temp < 30 or body_temp > 45:
            body_temp = DEFAULTS["body_temp"]

        return {
            "heart_rate": heart_rate,
            "spo2": spo2,
            "body_temp": body_temp,
        }

    except Exception:
        return {
            "heart_rate": DEFAULTS["heart_rate"],
            "spo2": DEFAULTS["spo2"],
            "body_temp": DEFAULTS["body_temp"],
        }

# ------------------------------
# Prediction Function
# ------------------------------

def predict_from_input(input_data):
    sensor_data = get_sensor_data()

    data_map = {
        "Age": float(input_data.get("age", DEFAULTS["age"])),
        "Sex": float(input_data.get("sex", DEFAULTS["sex"])),
        "Cholesterol": float(input_data.get("cholesterol", DEFAULTS["cholesterol"])),
        "Heart Rate": sensor_data["heart_rate"],
        "Diabetes": float(input_data.get("diabetes", DEFAULTS["diabetes"])),
        "Family History": float(input_data.get("family", DEFAULTS["family"])),
        "Smoking": float(input_data.get("smoke", DEFAULTS["smoke"])),
        "Alcohol Consumption": float(input_data.get("alcohol", DEFAULTS["alcohol"])),
        "Body Temperature": sensor_data["body_temp"],
        "Previous Heart Problems": float(input_data.get("prev_heart", DEFAULTS["prev_heart"])),
        "Medication Use": float(input_data.get("meds", DEFAULTS["meds"])),
        "Stress Level": float(input_data.get("stress", DEFAULTS["stress"])),
        "Physical Activity Days Per Week": float(input_data.get("activity", DEFAULTS["activity"])),
        "Sleep Hours Per Day": float(input_data.get("sleep", DEFAULTS["sleep"])),
        "Oxygen Saturation": sensor_data["spo2"],
        "Systolic_BP": float(input_data.get("sbp", DEFAULTS["sbp"])),
        "Diastolic_BP": float(input_data.get("dbp", DEFAULTS["dbp"])),
    }

    df = pd.DataFrame(
        [[data_map[col] for col in MODEL_COLUMNS]],
        columns=MODEL_COLUMNS,
    )

    scaled = scaler.transform(df)

    probability = model.predict_proba(scaled)[0][1]
    prob_percent = round(probability * 100, 2)

    # Risk classification
    if prob_percent < 30:
        risk_level = "Low"
    elif prob_percent < 60:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    prediction = int(probability >= 0.5)

    return {
        "prediction": prediction,
        "risk_probability": prob_percent,
        "risk_level": risk_level,
    }