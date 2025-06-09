import json
import os
import base64

import boto3

ATTENDANCE_TABLE_NAME = os.environ['ATTENDANCE_TABLE_NAME']
USER_TABLE_NAME       = os.environ['USER_TABLE_NAME']

def lambda_handler(event, context):
    # CORSヘッダーの設定
    cors_headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }

    try:
        # DynamoDBクライアント
        dynamodb = boto3.client('dynamodb')

        # クエリパラメータの取得とバリデーション
        query = event.get('queryStringParameters')
        if not query or 'id' not in query:
            # テーブル全件取得
            response = dynamodb.scan(TableName=ATTENDANCE_TABLE_NAME)
            items    = response.get('Items', [])
            # データが存在しない場合
            if not items:
                return {
                    'statusCode': 404,
                    'headers'   : cors_headers,
                    'body'      : json.dumps("No attendance records found.")
                }
            # Name, Statusのペアだけ抽出して返す
            results = [
                {
                    "name"  : item["Name"]["S"],
                    "status": item["Status"]["S"]
                } for item in items if "Name" in item and "Status" in item
            ]
            return {
                'statusCode': 200,
                'headers'   : cors_headers,
                'body'      : json.dumps(results)
            }

        # IDをデコード
        ID = base64.b64decode(query['id']).decode('utf-8')
        # DynamoDBからアイテムを取得
        response = dynamodb.get_item(
            TableName=USER_TABLE_NAME,
            Key={'ID': {'S': ID}}
        )
        # アイテムが存在しない場合の処理
        if "Item" not in response:
            return {
                'statusCode': 400,
                'headers'   : cors_headers,
                'body'      : json.dumps("User not found")
            }
        # アイテムが存在する場合の処理
        name = response['Item']['Name']['S']
        # 名前に対応する勤怠状態を取得
        response = dynamodb.get_item(
            TableName=ATTENDANCE_TABLE_NAME,
            Key={'Name': {'S': name}}
        )
        # 勤怠状態が存在しない場合の処理
        if "Item" not in response:
            return {
                'statusCode': 400,
                'headers'   : cors_headers,
                'body'      : json.dumps("Attendance record not found")
            }
        # 勤怠状態が存在する場合の処理
        status = response['Item']['Status']['S']
        return {
            'statusCode': 200,
            'headers'   : cors_headers,
            'body'      : json.dumps({"name": name, "status": status})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers'   : cors_headers,
            'body'      : json.dumps(f'Error: {str(e)}')
        }