import requests, time, json

from datetime import date


def get_weather():

    longitude = -3.1999
    latitude = 55.9486

    url = "https://api.open-meteo.com/v1/forecast"

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
        "timezone": "GMT",
        "forecast_days": 1,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    timestamp = int(time.time())

    return {
        "date": str(date.today()),
        "unix_timestamp": timestamp,
        "location": "Edinburgh",
        "raw": data,
    }


weather_data = get_weather()

with open("weather.json", "w") as f:
    json.dump(weather_data, f, indent=4)
