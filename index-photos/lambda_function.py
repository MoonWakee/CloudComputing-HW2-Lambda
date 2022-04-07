import json
import boto3
import requests
from requests.auth import HTTPBasicAuth

def lambda_handler(event, context):
    
    bucket = "cloud-computing-b2"
    print(event)
    key = event["Records"][0]["s3"]["object"]["key"]
    client = boto3.client("rekognition")
    # Hi
    
    response = client.detect_labels(
        Image = {"S3Object": {"Bucket": bucket, 'Name': key}}
        )
    
    label = response["Labels"] 
    labels = []
    
    for i in label:
        labels.append(i["Name"])
    
    head = boto3.client("s3").head_object(Bucket=bucket, Key=key)
    print(head)

    if head['Metadata']:
        custom_labels = head['Metadata']['customlabels'].split(',')
        for l in custom_labels:
            labels.append(l.strip())

    res = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": head['LastModified'].strftime("%Y-%m-%dT%H:%M:%S"),
        "labels": labels
    }
    
    print(res)
    
    url = 'https://search-photos-xp64xl7hwq5o6cy4w3qx2wmy7e.us-east-1.es.amazonaws.com/photos/_doc'
    payload = json.dumps(res)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=payload, headers=headers, auth=HTTPBasicAuth('master', 'Master123!'))
    print(r)

    '''
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept,x-amz-meta-customLabels',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET'
    '''
    

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept,x-amz-meta-customLabels',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,PUT'
        },
        "body": json.dumps(res)
    }
