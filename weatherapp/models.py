from django.db import models

class WeatherData(models.Model):
    city_name = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_name} - {self.date_time}"
