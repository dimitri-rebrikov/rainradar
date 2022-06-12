import boto3
import radolan_rv

db = boto3.resource("dynamodb")

def lambda_handler(event, context):
    rvTable = db.Table("rainradar_rv")
    plzDataMap = radolan_rv.radolanRvData()
    with rvTable.batch_writer() as batch:
        for plz, data in plzDataMap.items():
            batch.put_item(
                        Item={
                            'plz':plz,
                            'info': data
                        })