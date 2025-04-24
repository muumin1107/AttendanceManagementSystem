import os
import boto3
import csv
import io
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# リソース定義
dynamodb       = boto3.resource("dynamodb")
snapshot_table = dynamodb.Table(os.environ["SNAPSHOT_TABLE_NAME"])
s3             = boto3.client("s3")
s3_bucket      = os.environ["EXPORT_BUCKET_NAME"]

def lambda_handler(event, context):
    # スキャンで全件取得
    response = snapshot_table.scan()
    items    = response.get("Items", [])
    # JSTの日付（昨日分）
    now        = datetime.now(ZoneInfo("Asia/Tokyo"))
    export_day = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    # 日付でフィルタ（昨日分）
    filtered = [item for item in items if item.get("Date") == export_day]
    if not filtered:
        return {"statusCode": 200, "message": f"No data found for {export_day}"}

    # CSV文字列生成
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Name", "Timestamp", "Status", "Date", "Hour", "Weekday"])
    writer.writeheader()
    for row in filtered:
        writer.writerow({
            "Name"     : row.get("Name", ""),
            "Timestamp": row.get("Timestamp", ""),
            "Status"   : row.get("Status", ""),
            "Date"     : row.get("Date", ""),
            "Hour"     : row.get("Hour", ""),
            "Weekday"  : row.get("Weekday", "")
        })

    # S3キーを設定してアップロード
    key = f"snapshot/{export_day}.csv"
    s3.put_object(
        Bucket=s3_bucket,
        Key=key,
        Body=output.getvalue().encode("utf-8"),
        ContentType="text/csv"
    )

    return {"statusCode": 200, "message": f"Exported {len(filtered)} records for {export_day} to s3://{s3_bucket}/{key}"}