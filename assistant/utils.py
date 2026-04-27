"""Utility functions and command router for the assistant."""

import re

from assistant.app_launcher import open_app
from assistant.weather import get_current_date, get_current_time, parse_weather_query
from assistant.system_control import parse_system_command


def route_command(text: str) -> tuple:
    """Route user command to the appropriate handler.

    Returns:
        tuple: (response_text, command_type)
        command_type is one of: 'app', 'weather', 'time', 'date', 'system', 'ai'
    """
    text_lower = text.lower().strip()

    # Open app commands
    open_patterns = [
        r"^open\s+(.+)$",
        r"^launch\s+(.+)$",
        r"^start\s+(.+)$",
        r"^run\s+(.+)$",
    ]
    for pattern in open_patterns:
        match = re.match(pattern, text_lower)
        if match:
            app_name = match.group(1).strip()
            return open_app(app_name), "app"

    # Time queries
    time_patterns = [
        r"what('?s| is) the time",
        r"current time",
        r"tell me the time",
        r"what time is it",
    ]
    for pattern in time_patterns:
        if re.search(pattern, text_lower):
            return f"The current time is {get_current_time()}.", "time"

    # Date queries
    date_patterns = [
        r"what('?s| is) the date",
        r"what('?s| is) today",
        r"current date",
        r"tell me the date",
        r"what day is it",
    ]
    for pattern in date_patterns:
        if re.search(pattern, text_lower):
            return f"Today is {get_current_date()}.", "date"

    # Weather queries
    weather_patterns = [
        r"weather",
        r"temperature",
        r"how('?s| is) the weather",
        r"forecast",
    ]
    for pattern in weather_patterns:
        if re.search(pattern, text_lower):
            return parse_weather_query(text), "weather"

    # System control commands
    system_response = parse_system_command(text)
    if system_response:
        return system_response, "system"

    # Fall through to AI response
    return "", "ai"
