import csv
import json
import boto3
import io

client = boto3.client('s3')

def get_data(key, plz):
    for row in csv.reader(
        io.StringIO(
            client.get_object(
                Bucket='rainradar',
                Key=key
            )['Body'].read().decode()
        )
    ):
        if int(row[0]) == plz:
            return row[1:]


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

    mosmix_data = get_data('rainradar_rv_data', plz)
    if(mosmix_data):
        mosmix_data.append('00000000') # empty row between the data sets
        mosmix_data.extend(get_data('rainradar_mosmix_data', plz)) # add mosmix data
        return mosmix_data

    return {
        "statusCode": 404,
        "body": json.dumps({
            "error": "plz " + str(plz) + " not found"
        })
    }
