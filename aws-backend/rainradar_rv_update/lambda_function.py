import boto3
import radolan_rv

client = boto3.client('s3')

def lambda_handler(event, context):
    with radolan_rv.radolanRvDataStream() as file:
        client.put_object( 
            Bucket='rainradar',
            Body=file.read(),
            Key='rainradar_rv_data'
        )