from django.urls import path
from weatherapp.views import *

urlpatterns = [
    path('', weather_detail, name='weather_detail'),
    path('historical_weather/', historical_weather, name='historical_weather'),

]
