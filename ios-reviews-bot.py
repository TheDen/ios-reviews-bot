#!/usr/bin/env python3

import os
import sys
import requests
import json
import re

# Itunes application Id
AppId = '00000000'
endpoint='https://itunes.apple.com/AU/rss/customerreviews/id=' + AppId + '/sortBy=mostRecent/json'


# Grab the Slack webhook
try:
    os.environ['SLACKWEBHOOK']
except KeyError as e:
    # If you must hardcode the Slack webhook
    # SlackWebhook = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
    print('A valid Slack Webhook neeeds to be set as the envionment variable "SLACKWEBHOOK"\nExample: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX')
    sys.exit()
else:
    if re.search('https://hooks.slack.com/services/', os.environ['SLACKWEBHOOK']):
        SlackWebhook = os.environ['SLACKWEBHOOK']
    else:
        print('A valid Slack Webhook neeeds to be set as the envionment variable "SLACKWEBHOOK"\nExample: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX')
        sys.exit()

SlackChannel = '#bot-channel'
SlackUsername = 'iOS Reviews Bot'
SlackEmoji = ':iphone:'

# File to store all the Ids to date (absolute path)
IdFile='IDs'

req = requests.get(endpoint)
data = json.loads(req.text)

# Grab all the IDs
CurrentIds = []
for x in data['feed']['entry'][1:-1]:
    CurrentIds.append(x['id']['label'])


# Pull all the saved Ids into an array
AllIds = []
with open(IdFile) as f:
    AllIds = [line.rstrip() for line in f]


# Check if there are any new Ids
NewIds = []
for element in CurrentIds:
    if element not in AllIds:
        NewIds.append(element)

# Exit if there is nothing to update
if not NewIds:
      print('nothing to update')
      sys.exit()

# Grab data from the new Ids
NewData = []
for i in NewIds:
 NewData.append([item for item in data['feed']['entry']
        if item['id']['label'] == i])

# Build the payload for each Id
for idx, i in enumerate(NewData):
    review = i[0]['content']['label']
    author = i[0]['author']['name']['label']
    rating = i[0]['im:rating']['label']
    label = i[0]['title']['label']
    version = i[0]['im:version']['label']

    # Convert rating to emoji stars
    stars = ''
    for i in range(0,int(rating)):
        stars = stars + ':star:'

    SlackMessage = '_' + author + '_' + ' says:\n\n*' + label + '*\n' + review + '\n\n' + stars + '\nVersion ' + version
    SlackPayload = '{"channel": "' + SlackChannel + '", "text": ">>>' + SlackMessage + '", "username": "' + SlackUsername + '", "icon_emoji": "' + SlackEmoji + '"}'

    # Post payload to Slack Webhook
    response = requests.post(
        SlackWebhook, data=SlackPayload.replace('\n','\\n\r').encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        if response.status_code != 200:
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ReviewID: ', NewIds[idx]  , e)

# Append the new Ids to the IdFile
with open(IdFile, "a") as f:
    for i in NewIds:
        f.write(i+'\n')
    f.close
