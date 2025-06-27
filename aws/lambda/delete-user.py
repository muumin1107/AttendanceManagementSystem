import os
import json
import boto3

# 環境変数の取得
USER_TABLE_NAME       = os.environ.get('USER_TABLE_NAME')
ATTENDANCE_TABLE_NAME = os.environ.get('ATTENDANCE_TABLE_NAME')

# DynamoDBリソースの初期化
dynamodb = boto3.resource('dynamodb')

def _clear_table(table_name: str, primary_key_name: str) -> int:
    """指定されたDynamoDBテーブルの全アイテムを削除する関数"""
    if not table_name:
        return 0
    table = dynamodb.Table(table_name)

    try:
        # テーブルのスキャンを実行し，全アイテムのキーを取得
        scan_kwargs = {
            'ProjectionExpression': '#pk',
            'ExpressionAttributeNames': {
                '#pk': primary_key_name
            }
        }
        keys_to_delete = []

        # スキャンを繰り返して全アイテムを取得
        while True:
            response = table.scan(**scan_kwargs)
            items    = response.get('Items', [])
            keys_to_delete.extend(items)
            # 応答に 'LastEvaluatedKey' が含まれていない場合は終了（全アイテムを取得したため）
            if 'LastEvaluatedKey' not in response:
                break
            # 次のスキャンの開始位置を設定
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

        # 削除するアイテムのキーを整形
        item_count = len(keys_to_delete)
        if item_count > 0:
            # アイテムを削除するためのバッチ書き込みを実行
            with table.batch_writer() as batch:
                for key in keys_to_delete:
                    batch.delete_item(Key=key)
        else:
            print(f"No items found in table {table_name} to delete.")
        return item_count

    except Exception as e:
        print(f"Error clearing table {table_name}: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        # UserTableとAttendanceTableのアイテムを削除
        deleted_users_count      = _clear_table(USER_TABLE_NAME, 'ID')
        deleted_attendance_count = _clear_table(ATTENDANCE_TABLE_NAME, 'Name')

        # 成功メッセージの作成
        success_message = (
            f"Process completed successfully. "
            f"Deleted {deleted_users_count} items from UserTable and "
            f"{deleted_attendance_count} items from AttendanceTable."
        )
        return {
            'statusCode': 200,
            'body'      : json.dumps(success_message)
        }

    except Exception as e:
        print(f"An error occurred in the handler: {str(e)}")
        return {
            'statusCode': 500,
            'body'      : json.dumps(f'Error: {str(e)}')
        }