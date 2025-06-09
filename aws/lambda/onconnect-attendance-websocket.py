import os
import boto3
import time

# 環境変数を取得
CONNECTION_TABLE_NAME = os.environ['CONNECTION_TABLE_NAME']
VALID_API_KEY         = os.environ['VALID_API_KEY']

dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table(CONNECTION_TABLE_NAME)

def lambda_handler(event, context):
    try:
        # クライアントから送られてきたAPIキーをクエリパラメータから取得
        query_params = event.get('queryStringParameters', {})
        client_api_key = query_params.get('apiKey')
        # 正しいAPIキーと一致するか検証
        if client_api_key != VALID_API_KEY:
            print("API Key validation failed.")
            return {"statusCode": 403, "body": "Forbidden"}

        # 既存の接続処理
        connection_id = event["requestContext"]["connectionId"]
        timestamp = int(time.time())

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