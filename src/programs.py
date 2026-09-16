import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["PROGRAMS_TABLE"])

def lambda_handler(event, context):

    path_parameters = event.get("pathParameters") or {}
    program_id = path_parameters.get("programId")

    if program_id is not None:
        response = table.get_item(Key={"programId": program_id})
        program = response.get("Item")

        if program is None:
            return {
                "statusCode": 404,
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({"message": "Program not found"})
            }

        return {
                "statusCode": 200,
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({"program": program})
            }

    response = table.scan()
    program_records = response.get("Items", [])

    return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"programs": program_records})
        }