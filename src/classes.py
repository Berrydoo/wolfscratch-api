
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from datetime import datetime
from zoneinfo import ZoneInfo



dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["CLASSES_TABLE"])

def lambda_handler(event, context):
    path_parameters = event.get("pathParameters") or {}
    program_id = path_parameters.get("programId")

    if program_id is not None:

        today = datetime.now(ZoneInfo("America/New_York")).date().isoformat()

        response = table.query(
            IndexName="ClassesByProgram",
            KeyConditionExpression=Key("programId").eq(program_id),
            FilterExpression=(
                Attr("endsOn").gte(today)
                | Attr("endsOn").not_exists()
            )
        )
        classes = response.get("Items", [])
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"classes": classes})
        }

    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "programId is required"})
    }
