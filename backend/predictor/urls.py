from django.urls import path
from .views import predict_view, sensor_data_view

urlpatterns = [
    path('predict/', predict_view),
    path('sensor/', sensor_data_view),
]