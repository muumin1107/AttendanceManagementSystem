import json
import os
import boto3

TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    try:
        # DynamoDBクライアント
        dynamodb = boto3.client('dynamodb')

        # テーブル全件取得
        response = dynamodb.scan(TableName = TABLE_NAME)
        items    = response.get('Items', [])

        # データが存在しない場合
        if not items:
            return {'statusCode': 404, 'body': json.dumps("No attendance records found.")}

        # Name, Statusのペアだけ抽出して返す
        results = [
            {
                "name"  : item["Name"]["S"],
                "status": item["Status"]["S"]
            } for item in items if "Name" in item and "Status" in item # フィルタリング
        ]
        return {'statusCode': 200, 'body': json.dumps(results)}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}