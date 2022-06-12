import json
import boto3

db = boto3.resource("dynamodb")

def lambda_handler(event, context):
    assert 'queryStringParameters' in event, "missing plz parameter"
    queryParams = event['queryStringParameters']
    assert 'plz' in queryParams, "missing plz parameter"
    plz = int(queryParams['plz'])

    rvTable = db.Table("rainradar_rv")
    try:
        return rvTable.get_item(Key = {'plz':plz})['Item']["info"]
    except db.Client.exceptions.ResourceNotFoundException:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "plz " + str(plz) + " not found"
            })
        }
