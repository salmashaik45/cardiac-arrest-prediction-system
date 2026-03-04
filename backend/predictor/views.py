from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .utils import predict_from_input


# --------------------------------
# Render HTML Form
# --------------------------------

def form_view(request):
    return render(request, "predictor/form.html")


# --------------------------------
# Prediction API (CSRF Disabled)
# --------------------------------

@csrf_exempt
def predict_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = predict_from_input(data)
            return JsonResponse(result)

        except Exception as e:
            print("Prediction error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# --------------------------------
# Sensor Endpoint (Demo Values)
# --------------------------------

def sensor_data_view(request):
    return JsonResponse({
        "heart_rate": 80,
        "spo2": 95,
        "body_temp": 36.8
    })