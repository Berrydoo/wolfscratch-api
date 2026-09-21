
import json
import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["MEETINGS_TABLE"])

def lambda_handler(event, context):
    path_parameters = event.get("pathParameters") or {}
    class_id = path_parameters.get("classId")

    if class_id is None:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "classId is required"})
        }

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    response = table.query(
        IndexName="MeetingsByClass",
        KeyConditionExpression=(
            Key("classId").eq(class_id)
            & Key("startsAt").gte(now)
        ),
        ScanIndexForward=True
    )
    meetings = response.get("Items", [])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"meetings": meetings})
    }
