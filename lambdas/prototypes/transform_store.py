import json


def weathercode_risk_and_label(code):
    if code in (0, 1, 2, 3):
        return 0.0, "clear_or_cloudy"
    if code in (45, 48):
        return 0.3, "fog"
    if code in (51, 53, 55):
        return 0.2, "drizzle"
    if code in (56, 57):
        return 0.6, "freezing_drizzle"
    if code in (61, 63, 80, 81):
        return 0.4, "rain"
    if code in (65, 82):
        return 0.7, "heavy_rain"
    if code in (66, 67):
        return 0.8, "freezing_rain"
    if code in (71, 73, 77, 85):
        return 0.5, "snow"
    if code in (75, 86):
        return 0.8, "heavy_snow"
    if code == 95:
        return 0.8, "thunderstorm"
    if code in (96, 99):
        return 1.0, "thunderstorm_hail"
    return 0.0, "unknown"


def read_weather_json(filename="weather.json"):

    with open(filename, "r") as f:
        data = json.load(f)
    
    daily_data = data["raw"]["daily"]

    rain_risk = daily_data["precipitation_probability_max"][0] / 100.0

    wind_risk = min(daily_data["wind_gusts_10m_max"][0] / 70.0, 1.0)

    if daily_data["temperature_2m_min"][0] >= 0 and daily_data["temperature_2m_max"][0] <= 25:
        temp_risk = 0.0
    elif daily_data["temperature_2m_min"][0] < 0:
        temp_risk = min((0 - daily_data["temperature_2m_min"][0]) / 10.0, 1.0)
    else:
        temp_risk = min((daily_data["temperature_2m_max"][0] - 25.0) / 10.0, 1.0)

    wc_risk, wc_label = weathercode_risk_and_label(daily_data["weathercode"][0])

    raw_score = (
        0.4 * rain_risk +
        0.3 * wind_risk +
        0.2 * temp_risk +
        0.1 * wc_risk
        )
    
    risk_score = min(raw_score, 1.0)

    if risk_score < 0.3:
        risk_level = "LOW"
    elif risk_score < 0.7:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    db_item = {
        "unix_timestamp": data["unix_timestamp"],
        "date": data["date"],
        "location": data["location"],
        "temp_min": daily_data["temperature_2m_min"][0],
        "temp_max": daily_data["temperature_2m_max"][0],
        "temp_mean": daily_data["temperature_2m_mean"][0],
        "precip_prob_max": daily_data["precipitation_probability_max"][0],
        "wind_speed_max": daily_data["wind_speed_10m_max"][0],
        "wind_gust_max": daily_data["wind_gusts_10m_max"][0],
        "weathercode": daily_data["weathercode"][0],
        "wc_label": wc_label,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }

    print(json.dumps(db_item, indent=4))


read_weather_json()