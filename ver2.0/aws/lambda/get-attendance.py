import json
import os
import boto3

# 定数
BUCKET_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    try:
        # DynamoDB操作
        dynamodb = boto3.client('dynamodb')

        return {'statusCode': 200, 'body': json.dumps({"Attendance registered successfully."})}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}