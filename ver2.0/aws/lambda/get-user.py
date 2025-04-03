import json
import os
import base64
import boto3

# 定数
BUCKET_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    try:
        # クエリパラメータの取得とバリデーション
        query = event.get('queryStringParameters')
        if not query or 'id' not in query:
            return {'statusCode': 400, 'body': json.dumps("Missing 'id' parameter")}

        # IDのデコード
        ID = base64.b64decode(query['id']).decode('utf-8')

        # DynamoDB操作
        dynamodb = boto3.client('dynamodb')

        return {'statusCode': 200, 'body': json.dumps({'decoded_id': ID})}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}
