
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
    class_id = path_parameters.get("classId")

    if class_id is not None:
        response = table.get_item(Key={"classId": class_id})
        class_record = response.get("Item")

        if class_record is None:
            return {
                "statusCode": 404,
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({"message": "Class not found"})
            }

        return {
                "statusCode": 200,
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({"class": class_record})
            }


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
        "body": json.dumps({"message": "classId or programId is required"})
    }
