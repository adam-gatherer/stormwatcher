# lambdas/fetch_weather/logic.py

import time
from datetime import date
import json
import urllib.request
from urllib.parse import urlencode


def get_weather(
    api_url: str,
    latitude: float,
    longitude: float,
    timezone: str,
    forecast_days: int,
    location_name: str,
) -> dict:
    """Fetch daily forecast data for a single location and return a structured payload."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "temperature_2m_mean,"
            "precipitation_probability_max,"
            "wind_speed_10m_max,"
            "wind_gusts_10m_max,"
            "weathercode"
        ),
        "timezone": timezone,
        "forecast_days": forecast_days,
    }

    # Build full URL with encoded params
    url_with_params = f"{api_url}?{urlencode(params)}"

    # Perform HTTP GET (stdlib only)
    with urllib.request.urlopen(url_with_params, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        data = json.loads(body)

    timestamp = int(time.time())

    return {
        "date": str(date.today()),
        "unix_timestamp": timestamp,
        "location": location_name,
        "raw": data,
    }