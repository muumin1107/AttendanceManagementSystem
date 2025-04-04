import json
import os
import base64
import boto3
from botocore.exceptions import ClientError

# 定数
TABLE_NAME = os.environ['TABLE_NAME']

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
        ID   = base64.b64decode(event['id']).decode('utf-8')
        Name = base64.b64decode(event['name']).decode('utf-8')
        # データベース登録
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(
            TableName = TABLE_NAME,
            Item      = {
                'ID'  : {'S': ID},
                'Name': {'S': Name}
            },
            ConditionExpression='attribute_not_exists(ID)'
        )
        return {'statusCode': 200, 'body': json.dumps('User registered successfully.')}

    except ClientError as e:
        # 条件チェック失敗時の処理
        # 409 Conflict: ユーザーが既に存在する場合
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {'statusCode': 409, 'body': json.dumps('User already exists.')}
        else:
            return {'statusCode': 500, 'body': json.dumps(f'Error: {e.response["Error"]["Message"]}')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {e}')}