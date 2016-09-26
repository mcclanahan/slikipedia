import boto3
import json
import logging
import wikipedia
import requests
import urllib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    req_body = event['Records'][0]['Sns']['Message']
    params = params_to_dict(req_body)
    command_text = params['text']
    out_json = get_query_result(command_text)
    resp_url = urllib.unquote(params['response_url'].strip('"}'))
    send_response(resp_url, out_json)
    
def get_query_result(query):
    try:
        result = wikipedia.summary(query).encode('utf-8')
        page_info = get_page_info(query)
        out_json = {
            "attachments": 
            [
                {
                "thumb_url": page_info.images[0],
                "title": query.upper(),
                "title_link": page_info.url,
                "text": result,
                "mrkdwn_in": ["text"],
                "color": "#36a64f"
                }
            ]
        }
        return out_json

    except wikipedia.exceptions.DisambiguationError as error:
        #return possible terms if the query was too borad
        result = get_suggested_response(error.options, query)
        out_json = {
                "attachments": 
                    [       
                        {
                        "text": result,
                        "mrkdwn_in": ["text"],
                        "color": "warning"
                        }
                    ]
                }
        return out_json

    except wikipedia.exceptions.PageError as error:
        return get_notfound_response(query)

def get_page_info(query):
    #Return wikipedia page info from query
	fullpage =  wikipedia.page(query)
	return fullpage
   	
def get_suggested_response(options, query):
    header_text = "The search for *{}* was too broad, try one of these: \n{}"
    suggested_queries = get_suggested_options(options, 8)
    suggested_response = header_text.format(query, get_suggested_string(suggested_queries))
    #logger.error(suggested_response)
    return suggested_response


def get_notfound_response(query):
    #Format and respond to an invalid query
    result = "Sorry, {} could not be found. \n <https://www.google.com/search?q={}|Search Google for '{}'>".format(query,query,query)
    out_json = {
            "attachments": 
            [
                {
                "text": result,
                "mrkdwn_in": ["text"],
                "color": "danger"
                }
            ]
        }
    return out_json


def get_suggested_options(result, max_length):
    return result[:max_length]

def get_suggested_string(query):
    #find relavent terms if initial query was too broad
    suggested = ''
    for element in query:
        suggested += "\t{}\n".format(element)
    return suggested

def send_response(resp_url, out_json):
    #Returns info back to slack via resonse url in json
	r = requests.post(resp_url, data=json.dumps(out_json))

def params_to_dict(req_body):
    #Converts the incoming params to a dictionary 
    vals = {}
    for val in req_body.split('&'):
        k, v = val.split('=')
        vals[k] = v
    return vals        