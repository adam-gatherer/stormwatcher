# lambdas/fetch_weather/handler.py

import os
import json
import boto3


from .logic import get_weather

s3 = boto3.client("s3")


def lambda_handler(event, context):

    api_url = os.environ.get(
        "WEATHER_API_BASE_URL",
        "https://api.open-meteo.com/v1/forecast",
    )

    # defaults to Edinburgh Castle
    latitude = float(os.environ.get("LOCATION_LAT", "55.9486"))
    longitude = float(os.environ.get("LOCATION_LON", "-3.1999"))
    timezone = os.environ.get("TIMEZONE", "GMT")
    forecast_days = int(os.environ.get("FORECAST_DAYS", "1"))
    location_name = os.environ.get("LOCATION_NAME", "Edinburgh")

    raw_bucket = os.environ["RAW_BUCKET_NAME"]
    raw_prefix = os.environ.get("RAW_BUCKET_PREFIX", "raw/")

    payload = get_weather(
        api_url=api_url,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        forecast_days=forecast_days,
        location_name=location_name,
    )

    # s3 bucket key
    date_str = payload["date"]
    key = f"{raw_prefix}{date_str}-{location_name.lower()}.json"

    s3.put_object(
        Bucket=raw_bucket,
        Key=key,
        Body=json.dumps(payload).encode("utf-8"),
        ContentType="application/json",
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "bucket": raw_bucket,
                "key": key,
                "location": location_name,
                "date": date_str,
            }
        ),
    }