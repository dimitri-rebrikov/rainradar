import boto3
import mosmix_data

client = boto3.client('s3')

def lambda_handler(event, context):
    with mosmix_data.mosmixDataStream() as file:
        client.put_object( 
            Bucket='rainradar',
            Body=file.read(),
            Key='rainradar_mosmix_data'
        )