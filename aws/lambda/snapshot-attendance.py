import os
import boto3
from datetime import datetime, timezone, timedelta

# 環境変数を取得
ATTENDANCE_TABLE_NAME = os.environ.get('ATTENDANCE_TABLE_NAME')
SNAPSHOT_TABLE_NAME   = os.environ.get('SNAPSHOT_TABLE_NAME')

# boto3クライアントを初期化
dynamodb         = boto3.resource('dynamodb')
attendance_table = dynamodb.Table(ATTENDANCE_TABLE_NAME)
snapshot_table   = dynamodb.Table(SNAPSHOT_TABLE_NAME)

def lambda_handler(event, context):
    """AttendanceTableから全アイテムをスキャンし，AttendanceSnapshotTableにスナップショットを保存するLambda関数"""
    # --- 1. タイムスタンプを生成 ---
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)

    # スナップショットのパーティションキーとタイムスタンプを設定
    partition_date     = now.strftime('%Y-%m-%d')
    snapshot_timestamp = now.isoformat()
    print(f"Snapshotting for date: {partition_date} at {snapshot_timestamp}")

    # --- 2. AttendanceTableから全データをスキャン ---
    try:
        response         = attendance_table.scan()
        attendance_items = response.get('Items', [])
        print(f"Found {len(attendance_items)} items in {ATTENDANCE_TABLE_NAME}.")

    except Exception as e:
        print(f"Error scanning source table: {e}")
        return {'statusCode': 500, 'body': f"Error scanning source table: {e}"}

    if not attendance_items:
        print("No items to snapshot. Exiting.")
        return {'statusCode': 200, 'body': 'No items to snapshot.'}

    # --- 3. AttendanceSnapshotTableにバッチ書き込み ---
    try:
        with snapshot_table.batch_writer() as batch:
            for item in attendance_items:
                # 必要なキーが存在するか確認
                if 'Name' in item and 'Status' in item:
                    # スナップショットのユニークなソートキーを生成
                    unique_sort_key = f"{snapshot_timestamp}#{item['Name']}"

                    snapshot_item = {
                        'Date'     : partition_date,
                        'Timestamp': unique_sort_key,
                        'Name'     : item['Name'],
                        'Status'   : item['Status']
                    }
                    batch.put_item(Item=snapshot_item)
                else:
                    print(f"Skipping item due to missing 'Name' or 'Status': {item}")

        print(f"Successfully wrote {len(attendance_items)} items to {SNAPSHOT_TABLE_NAME}.")
        return {'statusCode': 200, 'body': 'Snapshot created successfully.'}

    except Exception as e:
        print(f"Error writing to target table: {e}")
        return {'statusCode': 500, 'body': f"Error writing to target table: {e}"}