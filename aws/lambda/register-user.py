import base64
import json
import os

import boto3
from botocore.exceptions import ClientError

# 定数
USER_TABLE_NAME = os.environ['USER_TABLE_NAME']
dynamodb        = boto3.client('dynamodb')

# ペイロードのバリデーション
def _is_valid_payload(payload: dict) -> bool:
    try:
        # 必要なキーが存在するかチェック
        required_keys = ['id', 'name', 'grade']
        if not all(key in payload for key in required_keys):
            return False
        # 各キーの型をチェック
        return (isinstance(payload['id'], str) and
                isinstance(payload['name'], str) and
                isinstance(payload['grade'], str))
    except (KeyError, TypeError):
        return False

def lambda_handler(event, context):
    try:
        # ペイロードの検証
        if not _is_valid_payload(payload = event):
            return {'statusCode': 400, 'body': json.dumps('The payload is invalid.')}

        # ペイロードの取得
        ID    = base64.b64decode(event['id']).decode('utf-8')
        Name  = base64.b64decode(event['name']).decode('utf-8')
        Grade = base64.b64decode(event['grade']).decode('utf-8')

        # DynamoDBにユーザー情報を登録
        dynamodb.put_item(
            TableName=USER_TABLE_NAME,
            Item={
                'ID'   : {'S': ID},
                'Name' : {'S': Name},
                'Grade': {'S': Grade}
            },
            ConditionExpression='attribute_not_exists(ID)'
        )
        return {'statusCode': 200, 'body': json.dumps('User registered successfully.')}

    except ClientError as e:
        # 条件チェック失敗時の処理
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {'statusCode': 409, 'body': json.dumps('User already exists.')}
        # その他のAWSクライアントエラー
        else:
            error_message = e.response.get("Error", {}).get("Message", "Unknown AWS Client Error")
            print(f"ClientError: {error_message}")
            return {'statusCode': 500, 'body': json.dumps(f'Error: {error_message}')}
    except json.JSONDecodeError:
        # bodyのJSONパース失敗時のエラー
        return {'statusCode': 400, 'body': json.dumps('Invalid JSON format in request body.')}
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}