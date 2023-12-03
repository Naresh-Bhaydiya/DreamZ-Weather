from django.contrib import admin
from weatherapp.models import *

@admin.register(WeatherData)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ['city_name','temperature','humidity','wind_speed','date_time']