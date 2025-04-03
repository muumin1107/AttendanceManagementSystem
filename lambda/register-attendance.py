import json
import os
import base64
import boto3

TABLE_NAME     = os.environ['TABLE_NAME']
VALID_STATUSES = {'clock_in', 'break_in', 'break_out', 'clock_out'}

def _is_valid_payload(payload: dict) -> bool:
    try:
        required_keys = ['name', 'status']
        # 必須キーの存在確認
        if not all(key in payload for key in required_keys):
            return False
        # 型チェック
        if not isinstance(payload['name'], str) or not isinstance(payload['status'], str):
            return False
        decoded_status = base64.b64decode(payload['status']).decode('utf-8')
        # ステータスのバリデーション
        if decoded_status not in VALID_STATUSES:
            return False
        return True
    except (KeyError, TypeError, base64.binascii.Error):
        return False

def lambda_handler(event, context):
    try:
        # ペイロードの検証
        if not _is_valid_payload(event):
            return {'statusCode': 400, 'body': json.dumps('Invalid payload or status.')}

        # ペイロードの取得
        Name   = base64.b64decode(event['name']).decode('utf-8')
        Status = base64.b64decode(event['status']).decode('utf-8')
        # データベース登録
        dynamodb = boto3.client('dynamodb')
        dynamodb.update_item(
            TableName                 = TABLE_NAME,
            Key                       = {'Name': {'S': Name}},
            UpdateExpression          = 'SET #s = :new_status',        # ステータスの更新
            ExpressionAttributeNames  = {'#s': 'Status'},              # ステータスの属性名
            ExpressionAttributeValues = {':new_status': {'S': Status}} # 新しいステータス
        )
        return {'statusCode': 200, 'body': json.dumps(f'Attendance status updated or registered successfully')}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}