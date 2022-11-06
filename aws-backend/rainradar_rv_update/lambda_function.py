from datetime import tzinfo
import boto3
import radolan_rv

client = boto3.client('s3')

def lambda_handler(event, context):

    rvTimestamp=radolan_rv.radolanRvTimeStamp()

    print("Timestamp of the latest radolan RV data:" + str(rvTimestamp))

    lastTimestamp=None
    try:
        lastTimestamp=client.get_object(
            Bucket='rainradar',
            Key='rainradar_rv_data'
        )['LastModified'].replace(tzinfo=None)
        print("Timestamp of the tast exectution:" + str(lastTimestamp))
    except client.exceptions.NoSuchKey:
        print("No last exectution")

    if lastTimestamp is None or rvTimestamp > lastTimestamp:
        print("Execute radolan data creation")
        with radolan_rv.radolanRvDataStream() as file:
            client.put_object( 
                Bucket='rainradar',
                Body=file.read(),
                Key='rainradar_rv_data'
            )
    else:
        print("No need to execute radolan data creation")