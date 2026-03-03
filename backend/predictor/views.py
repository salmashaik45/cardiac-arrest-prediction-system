import json
import os
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import predict_from_input


# -------------------------------------
# HTML Form View
# -------------------------------------

def form_view(request):
    return render(request, "predictor/form.html")


# -------------------------------------
# Prediction API
# -------------------------------------

@csrf_exempt
def predict_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = predict_from_input(data)

            return JsonResponse(result)

        except Exception as e:
            print("Prediction error:", e)
            return JsonResponse(
                {"error": "Prediction failed"},
                status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


# -------------------------------------
# Sensor API
# -------------------------------------

def sensor_data_view(request):
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    api_key = os.getenv("THINGSPEAK_API_KEY")

    # If environment variables missing
    if not channel_id or not api_key:
        return JsonResponse({
            "heart_rate": 80,
            "spo2": 95,
            "body_temp": 36.8
        })

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {"api_key": api_key, "results": 1}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("feeds"):
            raise Exception("No feed data")

        feed = data["feeds"][0]

        heart_rate = float(feed.get("field1", 80))
        spo2 = float(feed.get("field2", 95))
        body_temp = float(feed.get("field3", 36.8))

        # -------- VALIDATION --------
        if heart_rate <= 0 or heart_rate > 220:
            heart_rate = 80

        if spo2 <= 0 or spo2 > 100:
            spo2 = 95

        if body_temp < 30 or body_temp > 45:
            body_temp = 36.8
        # ----------------------------

        return JsonResponse({
            "heart_rate": round(heart_rate, 2),
            "spo2": round(spo2, 2),
            "body_temp": round(body_temp, 2)
        })

    except Exception as e:
        print("Sensor fetch error:", e)
        return JsonResponse({
            "heart_rate": 80,
            "spo2": 95,
            "body_temp": 36.8
        })