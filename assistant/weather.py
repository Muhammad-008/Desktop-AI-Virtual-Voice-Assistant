"""Weather, date, and time information module."""

import json
import urllib.request
import urllib.error
from datetime import datetime


def get_current_time() -> str:
    """Return the current time as a formatted string."""
    now = datetime.now()
    return now.strftime("%I:%M %p")


def get_current_date() -> str:
    """Return the current date as a formatted string."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y")


def get_datetime_info() -> str:
    """Return combined date and time information."""
    return f"Today is {get_current_date()}. The time is {get_current_time()}."


def get_weather(city: str = "London") -> str:
    """Fetch weather information for a city using wttr.in API (no API key needed)."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        humidity = current["humidity"]
        desc = current["weatherDesc"][0]["value"]
        feels_like_c = current["FeelsLikeC"]
        wind_speed = current["windspeedKmph"]

        return (
            f"Weather in {city}: {desc}. "
            f"Temperature: {temp_c}°C ({temp_f}°F), "
            f"feels like {feels_like_c}°C. "
            f"Humidity: {humidity}%, "
            f"Wind: {wind_speed} km/h."
        )
    except urllib.error.URLError:
        return f"Could not fetch weather data for {city}. Check your internet connection."
    except (KeyError, IndexError, json.JSONDecodeError):
        return f"Could not parse weather data for {city}."
    except Exception as e:
        return f"Error fetching weather: {e}"


def parse_weather_query(text: str) -> str:
    """Extract city from a weather query and return weather info."""
    text_lower = text.lower()
    city = "London"

    weather_keywords = ["weather in", "weather for", "weather at", "temperature in", "temperature for", "temperature at", "forecast in", "forecast for", "forecast at"]
    for keyword in weather_keywords:
        if keyword in text_lower:
            idx = text_lower.index(keyword) + len(keyword)
            city = text[idx:].strip().rstrip("?.!")
            break

    if city:
        return get_weather(city)
    return get_weather()
