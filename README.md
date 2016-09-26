# slikipedia - a serverless slackbot powered by AWS 

By harnessing the powers of AWS you can operate a serverless slackbot.  This bot is built using:
* Amazon API Gateway
* Amazon Lambda (two seperate functions)
* Amazon SNS

Now you’re thinking, why use two Lambda functions and SNS this could all be done in one function.  This is ture but you will run into issues with timeouts in Slack.  There is a 3 second timeout that can be beat sometimes but not always.  We want a reliable bot that doesn't return timeout errors on occasion.  The first Amazon Lambda function validates there is a term to search for and responds to the user immediately that the query is being processed.  It then publishes a message to Amazon SNS to handoff the user’s search.  This message is forwarded to the worker lambda function for processing as you can see in the Code flows below.












##Code flows
###Successful bot query
![successful](https://github.com/mcclanahan/slikipedia/blob/master/images/successful.png)

1. User uses slack command and a search term in Slack (/wiki iphone) which gets sent to Amazon API Gateway
2. AWS API Gateway accepts the request and sends it to the Amazon Lambda concierge function
3. The Amazon Lambda function does two things:
  * The function returns a message that the request is being serviced ("ok, looking up iphone..")
  * Sends the search request to Amazon SNS
4. Amazon SNS sends the message to the linked Amazon Lambda worker function
5. Amazon Lambda worker function queries wikipedia for the search term
6. The results are sent back to the worker function from Wikipedia
7. Results are formatted and return to the slack user


###Bot cannot find Wikipedia match
![failed](https://github.com/mcclanahan/slikipedia/blob/master/images/failed.png)

1. User uses slack command and a search term in Slack (/wiki g9is2ef ) which gets sent to Amazon API Gateway
2. AWS API Gateway accepts the request and sends it to the Amazon Lambda concierge function
3. The Amazon Lambda function does two things:
  * The function returns a message that the request is being serviced ("ok, looking up g9is2ef..")
  * Sends the search request to Amazon SNS
4. Amazon SNS sends the message to the linked Amazon Lambda worker function
5. Amazon Lambda worker function queries wikipedia for the search term
6. Wikipedia returns a failed lookup
7. Message is sent back to user that the term cannot be found and offers a link to Google for the search term (Sorry, g9is2ef could not be found. Search Google for 'g9is2ef') 

###Search term too vaugue
![vauge](https://github.com/mcclanahan/slikipedia/blob/master/images/vauge.png)

1. User uses slack command and a search term in Slack (/wiki tesla) which gets sent to Amazon API Gateway
2. AWS API Gateway accepts the request and sends it to the Amazon Lambda concierge function
3. The Amazon Lambda function does two things:
  * The function returns a message that the request is being serviced ("ok, looking up tesla..")
  * Sends the search request to Amazon SNS
4. Amazon SNS sends the message to the linked Amazon Lambda worker function
5. Amazon Lambda worker function queries wikipedia for the search term
6. Wikipedia returns up to eight suggested search terms based on the original vauge term 
7. Message is formatted and returned to user with the possible searhc options

###Empty search
![empty](https://github.com/mcclanahan/slikipedia/blob/master/images/empty_search.png)

1. User uses slack command but doesn't add a search term (/wiki ), blank request gets sent to Amazon API Gateway
2. AWS API Gateway accepts the request and sends it to the Amazon Lambda concierge function
3. The Amazon Lambda function does two things:
  * The function validates the empty search and returns "Great, now try to search for something." to the user 
  
