import os
import boto3
import csv
import io
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from boto3.dynamodb.conditions import Attr

# リソース定義
dynamodb       = boto3.resource("dynamodb")
snapshot_table = dynamodb.Table(os.environ["SNAPSHOT_TABLE_NAME"])
s3             = boto3.client("s3")
s3_bucket      = os.environ["EXPORT_BUCKET_NAME"]

def lambda_handler(event, context):
    # JSTの日付（昨日分）
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    export_day = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    # DynamoDB側で日付フィルタしてスキャン（ページネーション対応）
    items = []
    response = snapshot_table.scan(
        FilterExpression=Attr("Date").eq(export_day)
    )
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = snapshot_table.scan(
            FilterExpression=Attr("Date").eq(export_day),
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    if not items:
        return {"statusCode": 200, "message": f"No data found for {export_day}"}

    # CSV生成
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=["Name", "Timestamp", "Status", "Date", "Hour", "Weekday"])
    writer.writeheader()
    for row in items:
        writer.writerow({
            "Name"     : row.get("Name", ""),
            "Timestamp": row.get("Timestamp", ""),
            "Status"   : row.get("Status", ""),
            "Date"     : row.get("Date", ""),
            "Hour"     : row.get("Hour", ""),
            "Weekday"  : row.get("Weekday", "")
        })

    # S3アップロード
    key = f"snapshot/{export_day}.csv"
    s3.put_object(
        Bucket=s3_bucket,
        Key=key,
        Body='\ufeff' + output.getvalue(),
        ContentType="text/csv; charset=utf-8"
    )

    return {"statusCode": 200, "message": f"Exported {len(items)} records for {export_day} to s3://{s3_bucket}/{key}"}
