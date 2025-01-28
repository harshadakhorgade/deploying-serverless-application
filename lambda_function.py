import json
import os
import boto3
import urllib.parse

def lambda_handler(event, context):
    try:
        mypage = page_router(event['httpMethod'], event['queryStringParameters'], event['body'])
        return mypage
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def page_router(httpmethod, querystring, formbody):
    if httpmethod == 'GET':
        try:
            with open('contactus.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    elif httpmethod == 'POST':
        try:
            insert_record(formbody)
            with open('success.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }



def insert_record(formbody):
    # Decode URL-encoded formbody if necessary
    if isinstance(formbody, str) and "=" in formbody:
        formbody = dict(urllib.parse.parse_qsl(formbody))
    
    # Ensure formbody is a dictionary
    if not isinstance(formbody, dict):
        formbody = json.loads(formbody)

    # DynamoDB client
    client = boto3.client('dynamodb')

    # Define the table name
    table_name = "mydata"

    # Insert the data into DynamoDB
    response = client.put_item(
        TableName=table_name,
        Item={
            'fname': {'S': formbody['fname']},
            'lname': {'S': formbody['lname']},
            'email': {'S': formbody['email']},
            'message': {'S': formbody['message']}
        }
    )

    return response

