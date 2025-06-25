import base64
import json
import os

import boto3

ATTENDANCE_TABLE_NAME = os.environ['ATTENDANCE_TABLE_NAME']
VALID_STATUSES        = {'clock_in', 'break_in', 'break_out', 'clock_out'}

def _is_valid_payload(payload: dict) -> bool:
    try:
        required_keys = ['name', 'status']
        # 必須キーの存在確認
        if not all(key in payload for key in required_keys):
            return False
        # 型チェック
        if not isinstance(payload['name'], str) or not isinstance(payload['status'], str):
            return False
        # ステータスのバリデーション
        if payload['status'] not in VALID_STATUSES:
            return False
        return True
    except (KeyError, TypeError, base64.binascii.Error):
        return False

def lambda_handler(event, context):
    try:
        # ペイロードの検証
        if not _is_valid_payload(event):
            return {'statusCode': 400, 'body': json.dumps('Invalid payload. Required keys are "name" and "status".')}

        # ペイロードの取得
        Name   = base64.b64decode(event['name']).decode('utf-8')
        Status = base64.b64decode(event['status']).decode('utf-8')

        # DynamoDBのアイテムを更新
        dynamodb = boto3.resource('dynamodb')
        table    = dynamodb.Table(ATTENDANCE_TABLE_NAME)
        table.update_item(
            Key={'Name': Name},
            UpdateExpression='SET #s = :new_status',
            ExpressionAttributeNames={'#s': 'Status'},
            ExpressionAttributeValues={':new_status': Status}
        )
        return {'statusCode': 200, 'body': json.dumps(f"Attendance status for '{Name}' updated successfully to '{Status}'.")}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}