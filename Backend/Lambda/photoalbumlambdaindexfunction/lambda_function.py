# This has ci/cd 
import json
import boto3
import logging
import requests
from decimal import *
from requests_aws4auth import AWS4Auth

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Setting up elastic search endpoint for adding
region = 'us-east-1'
service = 'es'
credential = boto3.Session(aws_access_key_id="AKIAQ4GZLLQIBLG3FNGK",
                          aws_secret_access_key="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", 
                          region_name="us-east-1").get_credentials()
auth = AWS4Auth(credential.access_key, credential.secret_key, region, service)
esEndPoint = 'https://search-photos1-zbhe5jfrlsz7x4qqqupuv2avuy.us-east-1.es.amazonaws.com'
headers = { "Content-Type": "application/json" }
index = 'photoindex'
types = 'photo'
url = esEndPoint+ '/'+index+ '/'+types



def addToELasticSearch(dataToAdd):
    r = requests.post(url, auth=auth, json=dataToAdd, headers=headers)
    logger.info(r)
    logger.info(r.text)
    logger.info('successfully added to es')

def lambda_handler(event, context):
    logger.info(event)
    for record in event['Records']:
        print(record['s3'])
        # getting bucket name and image name from event
        bucketName = record['s3']['bucket']['name']
        keyName = record['s3']['object']['key']
        client = boto3.client('s3')
        response = client.head_object(Bucket=bucketName,Key=keyName)
        logger.info(response)
        
        logger.info('logging details for image'+ str(keyName))
        eventTime = record['eventTime']
        label = []
        # need to add custom labels
        if 'Metadata' in response:
            logger.info('has metadata')
            if 'customlabel' in response['Metadata']:
                logger.info('has customlabel')
                label = response['Metadata']['customlabel'].split(",")
                logger.info(label)
                logger.info(response['Metadata']['customlabel'])
        
        # for getting labels
        client = boto3.client('rekognition')
        rekogResponse = client.detect_labels(Image = {'S3Object': {'Bucket': bucketName, 'Name': keyName}})
        logger.info(rekogResponse)
        for tempLabels in rekogResponse['Labels']:
            label.append(tempLabels['Name'])
            logger.info(tempLabels['Name'])
        # assuming we have labels we will create json for adding to elastic search
        jsonBodyForES = {'objectKey': keyName,'bucket': bucketName,'createdTimestamp': eventTime,'labels': label}
        logger.info('successfully created json body')
        logger.info(jsonBodyForES)
        addToELasticSearch(jsonBodyForES)
        logger.info('done')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
