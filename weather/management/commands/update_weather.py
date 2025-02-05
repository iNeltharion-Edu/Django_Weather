from django.core.management.base import BaseCommand
from weather.services import update_weather

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        update_weather()
        self.stdout.write(self.style.SUCCESS("Weather updated successfully!"))
