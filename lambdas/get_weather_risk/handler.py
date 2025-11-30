import os
import json
import time

from datetime import datetime, timedelta, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["WEATHERRISK_TABLE_NAME"]
DEFAULT_LOCATION = os.environ.get("DEFAULT_LOCATION", "Edinburgh")


def _get_query_params(event):
    params = event.get("queryStringParameters") or {}
    location = params.get("location") or DEFAULT_LOCATION
    days_str = params.get("days") or "1"
    try:
        days = max(1, int(days_str))
    except ValueError:
        days = 1
    return location, days

