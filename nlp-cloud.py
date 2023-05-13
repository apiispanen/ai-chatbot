import nlpcloud
from AIWebService import app, apiconfig, config, helpers


client = nlpcloud.Client("fast-gpt-j", apiconfig.NLP_KEY, True)
# Returns a json object.

# print(client.intent_classification("Hello\nI'm looking for friends and can't find any. Can you help me?"))
# print(client.intent_classification("What events are happening in Harrisburg?"))
# print(client.intent_classification("What is going on this weekend in Harrisburg?"))
# print(client.intent_classification("Where would I find people to meet?"))
