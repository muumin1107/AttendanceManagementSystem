import json
import os
import boto3
from botocore.exceptions import ClientError

USER_TABLE_NAME = os.environ['USER_TABLE_NAME']
dynamodb        = boto3.client('dynamodb')

def lambda_handler(event, context):
    # CORS許可ヘッダー
    headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }

    try:
        # DynamoDBから全ユーザー情報を取得
        response = dynamodb.scan(TableName=USER_TABLE_NAME)
        items    = response.get('Items', [])

        # アイテムから重複を排除するための辞書を作成
        # 名前と学年の組み合わせで重複を排除
        unique_users_map = {}
        for item in items:
            name  = item.get('Name', {}).get('S')
            grade = item.get('Grade', {}).get('S')

            # 名前と学年が存在する場合のみ処理
            if name and grade and name not in unique_users_map:
                unique_users_map[name] = {
                    "name" : name,
                    "grade": grade
                }

        # 重複排除後のリストを作成
        deduplicated_list = list(unique_users_map.values())

        # 学年の優先度を定義
        grade_sort_order = {
            'RS': 0, # 研究員
            'M2': 1, # 修士2年
            'M1': 2, # 修士1年
            'B4': 3, # 学士4年
            'B3': 4  # 学士3年
        }

        # 学年と名前でソート
        # 学年の優先度をgrade_sort_orderから取得し、未定義の学年は末尾に配置
        sorted_list = sorted(
            deduplicated_list,
            key=lambda user: (
                grade_sort_order.get(user['grade'], 99), user['name']
            )
        )

        # 処理結果を返却
        return {
            'statusCode': 200,
            'headers'   : headers,
            'body'      : json.dumps(sorted_list)
        }

    except ClientError as e:
        error_message = e.response.get("Error", {}).get("Message", "Unknown AWS Client Error")
        print(f"ClientError: {error_message}")
        return {
            'statusCode': 500,
            'headers'   : headers,
            'body'      : json.dumps(f'Error: {error_message}')
        }
    except Exception as e:
        print(f"Unhandled error: {e}")
        return {
            'statusCode': 500,
            'headers'   : headers,
            'body'      : json.dumps(f'Error: {str(e)}')
        }