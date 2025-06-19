from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils import get_weather_data
from .models import SearchHistory
from channels.db import database_sync_to_async

@database_sync_to_async
def save_history(user, city):
    if user.is_authenticated:
        SearchHistory.objects.create(user=user, city=city)

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        city = data.get("city", "")
        weather = get_weather_data(city)

        await save_history(self.scope["user"], city)

        await self.send(text_data=json.dumps(weather))
