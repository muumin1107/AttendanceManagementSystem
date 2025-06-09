import os
import boto3

# 環境変数の取得
CONNECTION_TABLE_NAME = os.environ['CONNECTION_TABLE_NAME']

dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table(CONNECTION_TABLE_NAME)

def lambda_handler(event, context):
    try:
        connection_id = event["requestContext"]["connectionId"]

        # 削除
        table.delete_item(
            Key={"connectionId": connection_id}
        )

        return {"statusCode": 200, "body": "Disconnected"}

    except Exception as e:
        return {"statusCode": 500, "body": "Disconnection Failed.."}