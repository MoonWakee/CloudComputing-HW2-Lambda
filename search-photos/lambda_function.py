import json
import boto3
import requests
from requests.auth import HTTPBasicAuth

client = boto3.client('lambda')

def lambda_handler(event, context):
    client = boto3.client('lexv2-runtime')
    print(event)
    query = event['queryStringParameters']['q']
    print(query)
    
    if query == "":
        matches = []
        url = 'https://search-photos-xp64xl7hwq5o6cy4w3qx2wmy7e.us-east-1.es.amazonaws.com/photos/_doc/_search/?size=1000'
        
        r = requests.get(url, auth=HTTPBasicAuth('master', 'Master123!'))
        
        res = json.loads(r.text)
        print(res)
        if len(res['hits']['hits']) != 0:
            for hit in res['hits']['hits']:
                key = hit['_source']['objectKey']
                if key not in matches:
                    matches.append(key)
                    
        print(matches)
                    
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": str(matches)
        }
    
    response = client.recognize_text(
        botId='PTPLABFSWG',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text = query
    )
    
    queries = []
    if response['sessionState']['intent']['slots']['q1']:
        queries.append(response['sessionState']['intent']['slots']['q1']['value']['originalValue'])
    if response['sessionState']['intent']['slots']['q2']:
        queries.append(response['sessionState']['intent']['slots']['q2']['value']['originalValue'])
    if response['sessionState']['intent']['slots']['q3']:
        queries.append(response['sessionState']['intent']['slots']['q3']['value']['originalValue'])
    print(queries)
    
    matches = []
    for q in queries:
        if q[-1] == 's':
            q = q[:-1]
            print('new query: ' + q)
            
        url = 'https://search-photos-xp64xl7hwq5o6cy4w3qx2wmy7e.us-east-1.es.amazonaws.com/photos/_doc/_search?q=labels:' + q
        r = requests.get(url, auth=HTTPBasicAuth('master', 'Master123!'))
        
        res = json.loads(r.text)
        if len(res['hits']['hits']) != 0:
            for hit in res['hits']['hits']:
                key = hit['_source']['objectKey']
                if key not in matches:
                    matches.append(key)
    
    print(matches)
        
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": str(matches)
    }
