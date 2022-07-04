import csv
import json
import boto3
import io

client = boto3.client('s3')


def lambda_handler(event, context):
    if  'queryStringParameters' not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "missing plz parameter"
            })
        }
        
    queryParams = event['queryStringParameters']

    if 'plz' not in queryParams:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "missing plz parameter"
            })
        }

    plz = int(queryParams['plz'])

    for row in csv.reader(
        io.StringIO(
            client.get_object(
                Bucket='rainradar',
                Key='rainradar_rv_data'
            )['Body'].read().decode()
        )
    ):
        if int(row[0]) == plz:
            return row[1:]
    return {
        "statusCode": 404,
        "body": json.dumps({
            "error": "plz " + str(plz) + " not found"
        })
    }
