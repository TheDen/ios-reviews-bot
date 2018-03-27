#!/usr/bin/env python3

import os
import sys
import requests
import json
import re
import boto3

# Itunes application Id
AppId = 'XXXXXXXXX'
endpoint='https://itunes.apple.com/AU/rss/customerreviews/id=' + AppId + '/sortBy=mostRecent/json'

# AWS SSM Parameter Name
SSMParameter = 'slackwebhook-ssm'

SlackChannel = '#slack-channel'
SlackUsername = 'iOS Reviews Bot'
SlackEmoji = ':iphone:'

def getSlackWebhook(paramName):
  client = boto3.client('ssm')
  response = client.get_parameter(Name=paramName, WithDecryption=True)
  return response['Parameter']['Value']

def slackSend(NewData, NewIds):
  # Grab Slack Webhook
  SlackWebhook = getSlackWebhook(SSMParameter)

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

    # Set bar colour based on rating
    barcolor = 'good'
    if int(rating) < 3:
      barcolor = 'danger'
    elif int(rating) == 3:
      barcolor = 'warning'

    payload = {
    'channel': SlackChannel,
    'username': SlackUsername,
    'icon_emoji': SlackEmoji,
    'attachments': [{
      'author_name': author,
      'color': barcolor,
      'title': label,
      'text': review + '\n\n' + stars + '\nVersion ' + version
      }]
    }

    # Post payload to Slack Webhook
    response = requests.post(
        SlackWebhook, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    try:
      if response.status_code != 200:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      print('ReviewID: ', NewIds[idx]  , e)

def main():
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

  slackSend(NewData, NewIds)

  # Append the new Ids to the IdFile
  with open(IdFile, "a") as f:
    for i in NewIds:
      f.write(i+'\n')
    f.close

if __name__ == "__main__":
  main()
