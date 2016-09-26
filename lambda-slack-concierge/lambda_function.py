import boto3
import json
from base64 import b64decode
from urlparse import parse_qs

ENCRYPTED_EXPECTED_TOKEN = #ADD THE BASE-64 ENCODED ENCRYPTED SLACK COMMAND TOKEN
kms = boto3.client('kms')
sns = boto3.client('sns')
expected_token = kms.decrypt(CiphertextBlob = b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']
sns_arn = #ADD YOUR SNS ARN 

def lambda_handler(event, context):
    req_body = event['body']
    try:
        retval = {}        
        params = parse_qs(req_body)
        token = params['token'][0]
        if token != expected_token:
            logger.error("Request token (%s) does not match exptected", token)
            raise Exception("Invalid request token")
        wiki_query = params['text'][0]
        message = {
            "req_body": req_body
                    }
        sns_response = sns.publish(
            TopicArn=sns_arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
            )
        retval['text'] = "Ok, looking up {} ...".format(wiki_query)

    except Exception as e:
        retval['text'] = "Great, now try to search for something."

    return retval