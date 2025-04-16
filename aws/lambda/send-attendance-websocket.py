import boto3
import os
import json

# WebSocket APIのエンドポイント
WS_ENDPOINT = os.environ["WS_ENDPOINT"]
apigw = boto3.client("apigatewaymanagementapi", endpoint_url=WS_ENDPOINT)

# 接続管理用DynamoDB テーブル
dynamodb = boto3.resource("dynamodb")
table    = dynamodb.Table("ConnectionTable")

def lambda_handler(event, context):

    print("event:", json.dumps(event))

    for record in event.get("Records", []):
        if record.get("eventName") not in ["INSERT", "MODIFY"]:
            continue

        new_image = record["dynamodb"].get("NewImage", {})
        if "Name" not in new_image or "Status" not in new_image:
            continue

        name   = new_image["Name"]["S"]
        status = new_image["Status"]["S"]

        message = json.dumps({
            "name"  : name,
            "status": status
        })

        try:
            connections = table.scan().get("Items", [])
            for conn in connections:
                connection_id = conn.get("connectionId")
                print(connection_id)
                if not connection_id:
                    continue

                try:
                    apigw.post_to_connection(
                        ConnectionId = connection_id,
                        Data         = message.encode("utf-8")
                    )
                    print(f"Sent to {connection_id}")

                except apigw.exceptions.GoneException:
                    print(f"Stale connection: {connection_id}, deleting.")
                    table.delete_item(Key={"connectionId": connection_id})

        except Exception as e:
            print("Internal Server Error:", str(e))

    return {"statusCode": 200}