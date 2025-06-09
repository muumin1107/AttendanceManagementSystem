import boto3
import time

dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table("ConnectionTable")

def lambda_handler(event, context):
    try:
        connection_id = event["requestContext"]["connectionId"]
        timestamp = int(time.time())

        # 保存
        table.put_item(Item={
            "connectionId": connection_id,
            "timestamp"   : timestamp
        })

        return {"statusCode": 200, "body": "Connected!"}

    except KeyError as e:
        print(f"Missing expected key: {e}")
        return {"statusCode": 400, "body": "Bad Request"}

    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}