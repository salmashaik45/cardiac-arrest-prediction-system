from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import predict_from_input

# View to display the form
def form_view(request):
    return render(request, 'predictor/form.html')

# View to handle prediction API POST
@csrf_exempt
def predict_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        result = predict_from_input(data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
