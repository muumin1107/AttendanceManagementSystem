import os
import json
import boto3

USER_TABLE_NAME       = os.environ.get('USER_TABLE_NAME')
ATTENDANCE_TABLE_NAME = os.environ.get('ATTENDANCE_TABLE_NAME')

dynamodb = boto3.resource('dynamodb')

def _clear_table(table_name: str, primary_key_name: str) -> int:
    # テーブル名が設定されていない場合はスキップ
    if not table_name:
        print(f"Table name variable for '{primary_key_name}' is not set. Skipping.")
        return 0
    print(f"Starting to clear all items from table: {table_name}")
    table = dynamodb.Table(table_name)

    try:
        # プライマリキーの属性名を指定してスキャンする
        scan_kwargs = {'ProjectionExpression': primary_key_name}
        keys_to_delete = []
        # DynamoDBのスキャンを使用して全アイテムを取得
        while True:
            response = table.scan(**scan_kwargs)
            keys_to_delete.extend(response.get('Items', []))
            # 次のページがある場合はExclusiveStartKeyを設定
            if 'LastEvaluatedKey' not in response:
                break
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        # 削除するアイテムの数をカウント
        item_count = len(keys_to_delete)
        if item_count == 0:
            print(f"No items to delete in {table_name}.")
            return 0
        # バッチ処理でアイテムを削除
        with table.batch_writer() as batch:
            for key in keys_to_delete:
                batch.delete_item(Key=key)
        print(f"Successfully deleted {item_count} items from {table_name}.")
        return item_count

    except Exception as e:
        print(f"Error clearing table {table_name}: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        # UserTableをクリア
        deleted_users_count = _clear_table(USER_TABLE_NAME, 'ID')
        # AttendanceTableをクリア
        deleted_attendance_count = _clear_table(ATTENDANCE_TABLE_NAME, 'Name')
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
            'body'      : json.dumps(f'An error occurred during the cleanup process: {str(e)}')
        }