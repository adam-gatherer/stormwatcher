# lambdas/transform_store/handler.py

from __future__ import annotations
import json
import os
from typing import Any, Dict, List

import boto3

from logic import build_db_item

from decimal import Decimal


def convert_floats(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats(v) for v in obj]
    else:
        return obj


def send_status_notification(
    success: bool, item: dict | None, error: Exception | None = None
):
    """Send a 'write successful/failure' notification to STATUS_TOPIC_ARN."""
    # returns nothing to prevent faulty SNS attempt
    if not STATUS_TOPIC_ARN:
        return

    # build success message
    if success:
        subject = (
            f"Stormwatch write SUCCESS for {item.get('location')} {item.get('date')}"
        )
        message = {
            "status": "SUCCESS",
            "location": item.get("location"),
            "date": item.get("date"),
            "risk_score": item.get("risk_score"),
            "risk_level": item.get("risk_level"),
            "pk": item.get("PK"),
            "sk": item.get("SK"),
        }

    # build failure message
    else:
        subject = "Stormwatch write FAILURE"
        message = {
            "status": "FAILURE",
            "error": str(error),
        }
        # include partial context if we have it
        if item:
            message["location"] = item.get("location")
            message["date"] = item.get("date")

    # push message to SNS
    sns.publish(
        TopicArn=STATUS_TOPIC_ARN,
        Subject=subject,
        Message=json.dumps(message, default=str),
    )


def send_storm_notification(item: dict):
    """Send a 'storm incoming' notification to STORM_TOPIC_ARN if configured."""

    # returns nothing to prevent faulty SNS attempt
    if not STORM_TOPIC_ARN:
        return

    # builds storm message
    subject = f"Storm incoming: {item.get('location')} {item.get('date')} (risk={item.get('risk_level')})"
    message = {
        "location": item.get("location"),
        "date": item.get("date"),
        "risk_score": item.get("risk_score"),
        "risk_level": item.get("risk_level"),
        "temp_max": item.get("temp_max"),
        "precip_prob_max": item.get("precip_prob_max"),
        "wind_speed_max": item.get("wind_speed_max"),
        "wind_gust_max": item.get("wind_gust_max"),
        "weathercode": item.get("weathercode"),
        "wc_label": item.get("wc_label"),
    }

    # pushes message to SNS
    sns.publish(
        TopicArn=STORM_TOPIC_ARN,
        Subject=subject,
        Message=json.dumps(message, default=str),
    )


dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
sns = boto3.client("sns")

STATUS_TOPIC_ARN = os.environ.get("STATUS_TOPIC_ARN")
STORM_TOPIC_ARN = os.environ.get("STORM_TOPIC_ARN")
STORM_THRESHOLD = float(os.environ.get("STORM_THRESHOLD", "0.8"))


def get_table():
    table_name = os.environ["WEATHERRISK_TABLE_NAME"]
    return dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Triggered by S3 PUT events.

    For each new object:
      - read JSON from S3
      - transform to a risk item (build_db_item)
      - write into DynamoDB with PK/SK

    PK  = location uppercased (e.g. "EDINBURGH")
    SK  = unix_timestamp from the payload (number)
    """
    table = get_table()

    records: List[Dict[str, Any]] = event.get("Records", [])

    for record in records:
        # keep float copy for notifications
        item_for_notif = None

        try:
            s3_info = record["s3"]
            bucket = s3_info["bucket"]["name"]
            key = s3_info["object"]["key"]

            # reads the object from s3
            obj = s3.get_object(Bucket=bucket, Key=key)
            payload = json.loads(obj["Body"].read())

            # build the db item
            base_item = build_db_item(payload)

            # derive partition & sort key
            location = str(base_item.get("location", "EDINBURGH")).upper()
            unix_ts = int(base_item["unix_timestamp"])

            item = {
                "PK": location,
                "SK": unix_ts,
                **base_item,
            }

            # keep float version for notification
            item_for_notif = item.copy()

            # keep risk score before decimal conversion
            risk_score = item.get("risk_score")

            # convert floats to decimal for dynamodb
            item = convert_floats(item)

            # write to table
            table.put_item(Item=item)

            # success status
            send_status_notification(success=True, item=item_for_notif)

            # storm alert if above threshold
            if risk_score is not None and risk_score >= STORM_THRESHOLD:
                send_storm_notification(item_for_notif)

        except Exception as e:
            # failure status, include context
            send_status_notification(success=False, item=item_for_notif, error=e)
            # re-raise so lambda marked as failure
            raise

    return {"statusCode": 200}
