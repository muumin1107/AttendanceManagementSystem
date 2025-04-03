import json
import os
import base64
import boto3

# 定数
BUCKET_NAME = os.environ['TABLE_NAME']

# ペイロードのバリデーション
def _is_valid_payload(payload: dict) -> bool:
    try:
        # 必須キーの存在確認
        required_keys = ['id', 'name']
        if not all(key in payload for key in required_keys):
            return False
        # 型チェック
        return isinstance(payload['id'], str) and isinstance(payload['name'], str)
    except (KeyError, TypeError):
        return False

def lambda_handler(event, context):
    try:
        # ペイロードの検証
        if not _is_valid_payload(payload = event):
            return {'statusCode': 400, 'body': json.dumps('The payload is invalid.')}

        # ペイロードの取得
        ID   = base64.b64decode(event['id'])
        Name = base64.b64decode(event['name'])
        # データベース登録
        dynamodb = boto3.client('dynamodb')

        return {'statusCode': 200, 'body': json.dumps('User registered successfully.')}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {e}')}