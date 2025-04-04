import json
import os
import base64
import boto3

TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    try:
        # クエリパラメータの取得とバリデーション
        query = event.get('queryStringParameters')
        if not query or 'id' not in query:
            return {'statusCode': 400, 'body': json.dumps("Missing 'id' parameter")}

        # IDをデコード
        ID = base64.b64decode(query['id']).decode('utf-8')

        # DynamoDBからアイテムを取得
        dynamodb = boto3.client('dynamodb')
        response = dynamodb.get_item(
            TableName = TABLE_NAME,
            Key       = {
                'ID': {'S': ID}
            }
        )

        # アイテムが存在しない場合の処理
        if "Item" not in response:
            return {'statusCode': 400, 'body': json.dumps("User not found")}
        # アイテムが存在する場合の処理
        item = response['Item']
        return {'statusCode': 200, 'body': json.dumps({"name": item['Name']['S']})}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}