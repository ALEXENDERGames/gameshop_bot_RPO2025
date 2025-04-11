# weather.py
import requests
from config import WEATHER_API_KEY


def get_weather(city: str) -> str:
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "lang": "ru"  # Для ответа на русском
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            return f"❌ Ошибка: {data['error']['message']}"

        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]

        return (
            f"🌤 Погода в {location}:\n"
            f"• Температура: {temp_c}°C\n"
            f"• Состояние: {condition}\n"
            f"• Влажность: {humidity}%\n"
            f"• Ветер: {wind_kph} км/ч"
        )

    except Exception as e:
        return f"⚠️ Ошибка при запросе: {e}"# weather.py
import requests
from config import WEATHER_API_KEY

def get_weather(city: str) -> str:
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "lang": "ru"  # Для ответа на русском
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            return f"❌ Ошибка: {data['error']['message']}"

        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]

        return (
            f"🌤 Погода в {location}:\n"
            f"• Температура: {temp_c}°C\n"
            f"• Состояние: {condition}\n"
            f"• Влажность: {humidity}%\n"
            f"• Ветер: {wind_kph} км/ч"
        )

    except Exception as e:
        return f"⚠️ Ошибка при запросе: {e}"