import requests
from datetime import datetime, timedelta
from meteostat import Stations, Daily
import pandas as pd
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL

class WeatherAPI:
    def __init__(self):
        self.openweather_key = OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL

    def get_current_weather(self, city):
        """Fetch current weather data from OpenWeatherMap"""
        try:
            url = f"{self.base_url}/weather?q={city}&appid={self.openweather_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'rainfall': data.get('rain', {}).get('1h', 0),
                'clouds': data['clouds']['all']
            }
        except Exception as e:
            print(f"Error fetching current weather: {e}")
            return None

    def get_historical_weather(self, city, start_date, end_date):
        """Fetch historical weather data using Meteostat"""
        try:
            # Find nearest station
            stations = Stations()
            stations = stations.nearby(float(0), float(0))  # This is a placeholder - need actual lat/lon
            station = stations.fetch(1)

            if station.empty:
                return None

            # Fetch daily data
            data = Daily(station.index[0], start_date, end_date)
            data = data.fetch()

            return data
        except Exception as e:
            print(f"Error fetching historical weather: {e}")
            return None

    def get_forecast(self, city, days=5):
        """Get weather forecast"""
        try:
            url = f"{self.base_url}/forecast?q={city}&appid={self.openweather_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            forecast = []
            for item in data['list'][:days*8]:  # 8 entries per day
                forecast.append({
                    'date': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'rainfall': item.get('rain', {}).get('3h', 0),
                    'clouds': item['clouds']['all']
                })

            return forecast
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None
