from django.shortcuts import render
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import logging
import base64
import requests
from django.conf import settings
import matplotlib
matplotlib.use('Agg')
from weatherapp.models import *
import unittest

def get_weather_data(city_name):
    """
    Get weather data for a given city from the OpenWeatherMap API.
    Parameters:
    - city_name (str): Name of the city for which weather data is requested.
    Returns:
    - dict or None: Weather data in JSON format if successful, None otherwise.
    """
    try:
        api_key = settings.OPENWEATHERMAP_API_KEY
        base_url = settings.OPENWEATHERMAP_BASE_URL
        params = {'q': city_name, 'appid': api_key, 'units': 'metric'}  
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to get weather data for {city_name}. Status Code: {response.status_code}")
            return None
    except Exception as e:
        logging.exception(f"An exception occurred while getting weather data for {city_name}: {str(e)}")
        return None

class TestUtils(unittest.TestCase):
    """
    A test class for testing the get_weather_data function.
    """
    def test_get_weather_data_success(self,city_name):
        """
        Test the success case of the get_weather_data function.
        """
        if city_name != None:
            result = get_weather_data(city_name)
            self.assertIsNotNone(result)
        result = get_weather_data('NonexistentCity')
        self.assertIsNone(result)

def weather_detail(request):
    """
    View function for displaying current weather details and a bar chart.

    """
    try:
        if request.method == "POST":
            city_name = request.POST.get('city_name') 
            if not city_name:
                return render(request, 'weather/error.html', {'error_message': "City name is missing in the request."})            
            weather_data = get_weather_data(city_name)
            test_instance = TestUtils()
            test_instance.test_get_weather_data_success(city_name)
           
            if weather_data:
                temperature = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                WeatherData.objects.create(city_name=city_name, temperature=temperature, humidity=humidity, wind_speed=wind_speed)

                plt.bar(['Temperature', 'Humidity', 'Wind Speed'], [temperature, humidity, wind_speed])
                plt.title(f'Weather Information for {weather_data["name"]},')
                plt.xlabel('Metrics')
                plt.ylabel('Values')
    
                chart_image = BytesIO()
                plt.savefig(chart_image, format='png')
                chart_image.seek(0)
                plt.close()

                chart_base64 = base64.b64encode(chart_image.read()).decode('utf-8')

                return render(
                    request,
                    'weather/detail_with_chart.html',
                    {'weather_data': weather_data, 'chart_base64': chart_base64}
                )
            else:
                return render(request, 'weather/error.html', {'error_message': "Failed to retrieve weather data."})
            
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return render(request, 'weather/error.html', {'error_message': 'An error occurred. Please try again later.'})
    return render(request, 'weather/detail_with_chart.html', {'weather_data': '', 'chart_base64': ''})

def historical_weather(request):
    """
    View function for displaying historical weather data and a line chart.
    """
    if request.method == "POST":
        try:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            historical_data = WeatherData.objects.filter(
                date_time__range=[start_date, end_date]
            ).order_by('date_time')

            dates = [data.date_time for data in historical_data]
            temperatures = [data.temperature for data in historical_data]

            plt.plot(dates, temperatures, marker='o')
            plt.title('Temperature Trends Over Time')
            plt.xlabel('Date and Time')
            plt.ylabel('Temperature (°C)')

            chart_image = BytesIO()
            plt.savefig(chart_image, format='png')
            chart_image.seek(0)
            plt.close()            
            chart_base64 = base64.b64encode(chart_image.read()).decode('utf-8')
            return render(
                request,
                'weather/historical_weather.html',
                {'historical_data': historical_data, 'chart_base64': chart_base64}
            )
        except Exception as e:
            logging.exception(f"An exception occurred in the historical_weather view: {str(e)}")           
    return render(request, 'weather/historical_weather.html')
