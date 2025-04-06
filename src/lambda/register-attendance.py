import base64
import json
import os

import boto3

ATTENDANCE_TABLE_NAME = os.environ['ATTENDANCE_TABLE_NAME']
USER_TABLE_NAME       = os.environ['USER_TABLE_NAME']
VALID_STATUSES        = {'clock_in', 'break_in', 'break_out', 'clock_out'}

def _is_valid_payload(payload: dict) -> bool:
    try:
        required_keys = ['id', 'status']
        # 必須キーの存在確認
        if not all(key in payload for key in required_keys):
            return False
        # 型チェック
        if not isinstance(payload['id'], str) or not isinstance(payload['status'], str):
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
        ID     = base64.b64decode(event['id']).decode('utf-8')
        Status = base64.b64decode(event['status']).decode('utf-8')
        # IDに対応するNameを取得
        dynamodb = boto3.client('dynamodb')
        response = dynamodb.get_item(
            TableName = USER_TABLE_NAME,
            Key       = {
                'ID': {'S': ID}
            }
        )
        # アイテム（Name）が存在しない場合の処理
        if "Item" not in response:
            return {'statusCode': 400, 'body': json.dumps("User not found")}

        # データベース登録
        Name = response['Item']['Name']['S']
        dynamodb.update_item(
            TableName                 = ATTENDANCE_TABLE_NAME,
            Key                       = {'Name': {'S': Name}},
            UpdateExpression          = 'SET #s = :new_status',        # ステータスの更新
            ExpressionAttributeNames  = {'#s': 'Status'},              # ステータスの属性名
            ExpressionAttributeValues = {':new_status': {'S': Status}} # 新しいステータス
        )
        return {'statusCode': 200, 'body': json.dumps(f'Attendance status updated or registered successfully')}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}