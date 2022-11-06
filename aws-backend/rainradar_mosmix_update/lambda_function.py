import boto3
import mosmix_data

client = boto3.client('s3')

def lambda_handler(event, context):
    mosmixTimestamp=mosmix_data.mosmixDataTimeStamp()

    print("Timestamp of the latest mosmix data:" + str(mosmixTimestamp))

    lastTimestamp=None
    try:
        lastTimestamp=client.get_object(
            Bucket='rainradar',
            Key='rainradar_mosmix_data'
        )['LastModified'].replace(tzinfo=None)
        print("Timestamp of the last exectution:" + str(lastTimestamp))
    except client.exceptions.NoSuchKey:
        print("No last exectution")

    if lastTimestamp is None or mosmixTimestamp > lastTimestamp:
        with mosmix_data.mosmixDataStream() as file:
            client.put_object( 
                Bucket='rainradar',
                Body=file.read(),
                Key='rainradar_mosmix_data'
            )
    else:
        print("No need to execute mosmix data creation")