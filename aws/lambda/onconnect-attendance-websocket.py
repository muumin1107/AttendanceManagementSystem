import os
import boto3
import datetime

# 環境変数を取得
CONNECTION_TABLE_NAME = os.environ['CONNECTION_TABLE_NAME']

dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table(CONNECTION_TABLE_NAME)

def lambda_handler(event, context):
    try:
        # 既存の接続処理
        connection_id = event["requestContext"]["connectionId"]
        # 日本時間
        timestamp     = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S"))

        # DynamoDBに保存
        table.put_item(Item={
            "connectionId": connection_id,
            "timestamp"   : timestamp
        })

        return {"statusCode": 200, "body": "Connected!"}

    except KeyError as e:
        print(f"Missing expected key in event payload: {e}")
        return {"statusCode": 400, "body": "Bad Request"}

    except Exception as e:
        print(f"Unhandled error: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}