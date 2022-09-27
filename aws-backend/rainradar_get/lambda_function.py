import csv
import json
from time import strftime
import boto3
import io
from datetime import datetime

client = boto3.client('s3')

def get_data(key, plz):
    file = client.get_object(
        Bucket='rainradar',
        Key=key
    )
    for row in csv.reader(
        io.StringIO(
            file['Body'].read().decode()
        )
    ):
        if int(row[0]) == plz:
            return {
                "values":row[1:], 
                "timestamp":file['LastModified']
                }

def create_response(http_code, response_object, last_modified=None):
    return {
        "isBase64Encoded": False,
        "statusCode": http_code,
        "headers": {
            "content-type": "application/json",
            "last-modified": last_modified.strftime('%a, %d %b %Y %X %Z') if last_modified is not None else None
        },
        "body": json.dumps(response_object)
    }

def lambda_handler(event, context):
    if  'queryStringParameters' not in event:
        return create_response(400, {
                "error": "missing plz parameter"
        })

    queryParams = event['queryStringParameters']

    if 'plz' not in queryParams:
        return create_response(400, {
            "error": "missing plz parameter"
        })

    try:
        plz = int(queryParams['plz'])
    except ValueError:
        return create_response(400, {
            "error": "wrong plz value"
        })

    rainradar_data = get_data('rainradar_rv_data', plz)
    if(rainradar_data):
        values = rainradar_data['values']
        values.append('00000000') # empty row between the data sets
        values.extend(get_data('rainradar_mosmix_data', plz)['values']) # add mosmix data
        return create_response(200, values, rainradar_data['timestamp'])

    return create_response( 404,{
        "error": "plz " + str(plz) + " not found"
    })
