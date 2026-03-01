from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
from .utils import predict_from_input


# ---------- Form Page ----------
def form_view(request):
    return render(request, 'predictor/form.html')


# ---------- Prediction API ----------
@csrf_exempt
@csrf_exempt
def predict_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        result = predict_from_input(data)
        return JsonResponse(result)

    except Exception as e:
        print("Prediction error:", e)
        raise e


# ---------- Sensor Data API ----------
def sensor_data_view(request):
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    api_key = os.getenv("THINGSPEAK_API_KEY")

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {"api_key": api_key, "results": 1}

    try:
        response = requests.get(url, params=params).json()
        feed = response['feeds'][0]
        return JsonResponse({
            "heart_rate": feed['field1'],
            "spo2": feed['field2'],
            "body_temp": feed['field3']
        })
    except Exception as e:
        print("Prediction error:", e)
        raise e