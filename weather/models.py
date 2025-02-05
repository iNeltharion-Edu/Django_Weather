from django.db import models

class CityWeather(models.Model):
    city = models.CharField(max_length=100, unique=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)
    time = models.CharField(max_length=10, default="00:00")
    forecast = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C ({self.time})"
