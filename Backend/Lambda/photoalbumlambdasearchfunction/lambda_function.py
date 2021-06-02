import boto3
import json
import requests
import random
from requests_aws4auth import AWS4Auth
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
S3url = "https://photoalbumassignment2storingphotoctsn.s3.amazonaws.com/"

def lambda_handler(event, context):
    logger.info('printing event')
    logger.info(event)
    print(event)
    print("event is", event['params']['querystring']['q'])
    q = event['params']['querystring']['q']

    client = boto3.client('lex-runtime')
    response = client.post_text(botName='searchBot', botAlias='searchbot', userId='300', inputText=q)
    slots = response['slots']
    print(slots)
    print(response)
    listoflabels = []
    for key in slots:
        if not slots[key]:
            continue
        listoflabels.append(slots[key])
    print(slots)
    print('listoflabels')
    print(listoflabels)
    
    
    #auth
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session(aws_access_key_id="",
                          aws_secret_access_key="", 
                          region_name="us-east-1").get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    esEndPoint = 'https://search-photos1-zbhe5jfrlsz7x4qqqupuv2avuy.us-east-1.es.amazonaws.com'
    headers = { "Content-Type": "application/json" }
    index = 'photoindex'
    types = 'photo'
    url = esEndPoint+ '/'+index + '/_search'
    headers = { "Content-Type": "application/json" }
    
    allObjects = []
    
    for x in listoflabels:
        query = {"size": 1300, "query": {"query_string": {"default_field": "labels", "query": x} }}
        print("query is ", query)
        response = requests.get(url,auth=awsauth, headers=headers, data=json.dumps(query))
        res = response.json()
        logger.info(res)
        hits = res['hits']['hits']
        print("hits " + x, hits)
        
        for hit in hits:
            allObjects.append(str(hit['_source']['objectKey']))
    
    allObjects = list(set(allObjects))
    imagesToSend = []
    for x in allObjects:
        imagesToSend.append(S3url+x)
    imagesToSend = list(set(imagesToSend))
    print(imagesToSend)

    return {
        'statusCode': 200,
        'body': json.dumps(imagesToSend),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },

    }


