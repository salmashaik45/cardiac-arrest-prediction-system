from django.urls import path
from .views import form_view, predict_view

urlpatterns = [
    path('form/', form_view),         # Show HTML form
    path('predict/', predict_view),   # API endpoint
]
