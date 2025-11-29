# lambdas/transform_store/handler.py

from __future__ import annotations
import json
import os
from typing import Any, Dict, List

import boto3

from logic import build_db_item

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")


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
        s3_info = record["s3"]
        bucket = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]

        # reads the object from s3
        obj = s3.get_object(Bucket=bucket, Key=key)
        payload = json.loads(obj["Body"].read())

        # build the db item
        base_item = build_db_item(payload)

        # derrive partition & sort key
        location = str(base_item.get("location", "EDINBURGH")).upper()
        unix_ts = int(base_item["unix_timestamp"])

        item = {
            "PK": location,     # e.g. "EDINBURGH"
            "SK": unix_ts,      # sort key = unix timestamp
            **base_item,
        }

        # write to table
        table.put_item(Item=item)


    return {"statusCode": 200}