import boto3
import json

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserDB')
        count = event['queryStringParameters']['count']
        new_item = {
            'time': 0,
            'count': int(count)+1
        }
        # カウントを更新
        _ = table.put_item(Item=new_item)
        return {'statusCode': 200, 'body': json.dumps({'Success': 'Data'})}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}