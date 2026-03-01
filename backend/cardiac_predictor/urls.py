from django.contrib import admin
from django.urls import path, include
from predictor.views import form_view

urlpatterns = [
    path('', form_view, name='home'),   # Root shows form
    path('admin/', admin.site.urls),
    path('api/', include('predictor.urls')),
]