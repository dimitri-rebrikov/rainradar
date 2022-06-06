import json
import rainradar

def lambda_handler(event, context):
    queryParams = event['queryStringParameters']
    try:
        if 'plz' in queryParams:
            return json.dumps(rainradar.rainradarForPlz(queryParams['plz']))
        elif 'lat' in queryParams and 'lon' in queryParams:
            return json.dumps(rainradar.rainradarForCoord(lat=queryParams['lat'], lon=queryParams['lon']))
        else:
            assert False, "missing plz or lat/lon parameters"
    except AssertionError as msg:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(msg)
            })
        }


if __name__ == "__main__":
    # wrong parameter simulation 
    # print(lambda_handler({
    #     "queryStringParameters": {
    #         "parameter1": "value1,value2",
    #         "parameter2": "value"
    #     }
    # }, None))
    #
    # plz parameter simulation 
    print(lambda_handler({
        "queryStringParameters": {
            "plz": "70567"
        }
    }, None))
    #
    # lat/lob parameter simulation 
    # print(lambda_handler({
    #     "queryStringParameters": {
    #         'lat' : '52.4036560155822', 
    #         'lon' : '9.771084486390333'
    #     }
    # }, None))