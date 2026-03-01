import joblib
import pandas as pd
import requests

# Load model and scaler
model = joblib.load('predictor/best_model.pkl')
scaler = joblib.load('predictor/scaler.pkl')

DEFAULTS = {
    'age': 40,
    'sex': 1,
    'cholesterol': 190,
    'heart_rate': 80,
    'diabetes': 0,
    'family': 0,
    'smoke': 0,
    'alcohol': 0,
    'body_temp': 36.8,
    'prev_heart': 0,
    'meds': 0,
    'stress': 5,
    'activity': 3,
    'sleep': 7,
    'spo2': 95,
    'sbp': 120,
    'dbp': 80,
}

FEATURE_ORDER = list(DEFAULTS.keys())

def get_sensor_data():
    url = "https://api.thingspeak.com/channels/3017666/feeds.json"
    params = {"api_key": "GF8053OVJNAFFLJ6", "results": 1}
    try:
        response = requests.get(url, params=params).json()
        feed = response['feeds'][0]
        return {
            'heart_rate': float(feed['field1']),
            'spo2': float(feed['field2']),
            'body_temp': float(feed['field3']),
        }
    except:
        return {
            'heart_rate': DEFAULTS['heart_rate'],
            'spo2': DEFAULTS['spo2'],
            'body_temp': DEFAULTS['body_temp'],
        }

def predict_from_input(input_data):
    sensor_data = get_sensor_data()
    used_defaults = []
    row = []

    for key in FEATURE_ORDER:
        if key in sensor_data:
            val = sensor_data[key]
        else:
            val = input_data.get(key)
            if val in [None, '', 'null', 'None']:
                val = DEFAULTS[key]
                used_defaults.append(key)
        row.append(float(val))

    df = pd.DataFrame([row], columns=FEATURE_ORDER)
    scaled = scaler.transform(df)
    prediction = int(model.predict(scaled)[0])

    return {
        'prediction': prediction,
        'used_defaults': used_defaults
    }
