import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["PROGRAMS_TABLE"])

def lambda_handler(event, context):

    response = table.scan()
    program_records = response.get("Items", [])

    return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"programs": [program_records]})
        }