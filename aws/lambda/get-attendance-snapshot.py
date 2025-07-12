import os
import json
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
from collections import defaultdict

# 環境変数からテーブル名を取得
SNAPSHOT_TABLE_NAME       = os.environ.get('SNAPSHOT_TABLE_NAME')
SNAPSHOT_INTERVAL_MINUTES = 60 # スナップショット間隔（分）

# boto3クライアントを初期化
dynamodb       = boto3.resource('dynamodb')
snapshot_table = dynamodb.Table(SNAPSHOT_TABLE_NAME)

def lambda_handler(event, context):
    """指定された期間の在室記録スナップショットを集計し，ユーザーごと・日付ごとの合計在室時間（分）を計算して返す．"""
    # CORSヘッダーの設定
    cors_headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }

    params = event.get('queryStringParameters', {})
    if not params or 'startDate' not in params or 'endDate' not in params:
        return {'statusCode': 400, 'headers': cors_headers, 'body': json.dumps({'error': 'Missing required query parameters: startDate and endDate'})}

    start_date_str = params['startDate']
    end_date_str   = params['endDate']
    user_name      = params.get('userName')

    # --- 1. 指定された日付範囲の全スナップショットを取得 ---
    all_items = []
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date   = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        current_date = start_date
        while current_date <= end_date:
            date_str     = current_date.strftime('%Y-%m-%d')
            query_kwargs = {'KeyConditionExpression': Key('Date').eq(date_str)}

            if user_name:
                query_kwargs['FilterExpression'] = Attr('Name').eq(user_name)

            response = snapshot_table.query(**query_kwargs)
            all_items.extend(response.get('Items', []))
            while 'LastEvaluatedKey' in response:
                query_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = snapshot_table.query(**query_kwargs)
                all_items.extend(response.get('Items', []))
            current_date += timedelta(days=1)

    except ValueError:
        return {'statusCode': 400, 'headers': cors_headers, 'body': json.dumps({'error': 'Invalid date format. Please use YYYY-MM-DD.'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': f'Failed to retrieve data from database: {e}'})}

    # --- 2. ユーザーごと・日付ごとの在室スナップショット数を集計 ---
    daily_counts = defaultdict(lambda: defaultdict(int))
    for item in all_items:
        if item.get('Status') == 'clock_in':
            daily_counts[item['Name']][item['Date']] += 1

    # --- 3. 集計結果を合計分数に変換 ---
    attendance_by_user = defaultdict(dict)
    for name, date_counts in daily_counts.items():
        for date, count in date_counts.items():
            total_minutes = count * SNAPSHOT_INTERVAL_MINUTES
            attendance_by_user[name][date] = total_minutes

    # --- 4. レスポンスを生成 ---
    return {
        'statusCode': 200,
        'headers'   : cors_headers,
        'body'      : json.dumps(attendance_by_user, ensure_ascii=False)
    }