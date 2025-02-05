from django.shortcuts import render
from .models import CityWeather

def weather_view(request):
    cities = CityWeather.objects.all()
    return render(request, "weather/index.html", {"cities": cities})
