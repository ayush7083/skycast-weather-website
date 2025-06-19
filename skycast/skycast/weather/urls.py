from django.urls import path
from .views import weather_api, home  # Renamed to match updated function

urlpatterns = [
    path('', home, name='home'),  # Home page with weather form and history
    path('api/weather/', weather_api, name='weather_api'),  # Correct endpoint name
]
