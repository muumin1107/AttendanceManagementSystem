import boto3

dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table("ConnectionTable")

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