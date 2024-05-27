import json
import boto3
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    # Process the S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Get the object
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Process the content and insert into DynamoDB
        table.put_item(Item={'id': key, 'content': content})

    return {
        'statusCode': 200,
        'body': json.dumps('File processed and data inserted into DynamoDB')
    }
