import os
import boto3
from datetime import datetime
import pytz

dynamodb         = boto3.resource("dynamodb")
attendance_table = dynamodb.Table(os.environ["ATTENDANCE_TABLE_NAME"])
snapshot_table   = dynamodb.Tabel(os.environ["SNAPSHOT_TABLE_NAME"])

def lambda_handler(event, context):
    now      = datetime.now(pytz.timezone("Asia/Tokyo"))
    iso_ts   = now.isofotmat()
    date_str = now.strftime("%Y-%m-%d")
    hour     = now.hour
    weekday  = now.strftime("%A")

    # 現在の全ユーザー状態取得
    response = attendance_table.scan()
    items    = response.get("Items", [])

    for item in items:
        snapshot_table.put_item(Item={
            "Name"     : item["Name"],
            "Timestamp": iso_ts,
            "Status"   : item["Status"],
            "Date"     : date_str,
            "Hour"     : hour,
            "Weekday"  : weekday
        })

    return {"statu": "OK", "recorded": len(items)}