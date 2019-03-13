#!/usr/bin/env python3

import boto3
import json
import redis
import requests
import time


def getSSMparam(SSMparam):
    client = boto3.client("ssm")
    response = client.get_parameter(Name=SSMparam, WithDecryption=True)
    return response["Parameter"]["Value"]


def slackSend(
    SSMParameter,
    SlackWebhook,
    SlackChannel,
    SlackUsername,
    SlackEmoji,
    reviewcontent,
    author,
    rating,
    label,
    version,
):

    # Convert rating to emoji stars
    stars = ""
    for i in range(0, int(rating)):
        stars = stars + ":star:"

    # Set bar colour based on rating
    barcolor = "good"
    if int(rating) < 3:
        barcolor = "danger"
    elif int(rating) == 3:
        barcolor = "warning"

    payload = {
        "channel": SlackChannel,
        "username": SlackUsername,
        "icon_emoji": SlackEmoji,
        "attachments": [
            {
                "author_name": author,
                "color": barcolor,
                "title": label,
                "text": reviewcontent + "\n\n" + stars + "\nVersion " + version,
            }
        ],
    }

    response = requests.post(headers={"Content-Type": "application/json"})


def getreviews(endpoint):
    req = requests.get(endpoint)
    data = json.loads(req.text)
    return data


def redisconnect(host, port, password):
    return redis.Redis(host=host, port=port, password=password)


def handler(event, context):

    RedisSSMParameter = "redispw-SSMparam"
    redispw = getSSMparam(RedisSSMParameter)
    r = redisconnect("redis-host", 12345, redispw)

    SlackSSMParameter = "slackwebhook-SSMparam"
    SlackChannel = "@denis.khoshaba"
    SlackUsername = "iOS Reviews Bot"
    SlackEmoji = ":iphone:"
    SlackWebhook = getSSMparam(SlackSSMParameter)

    # Itunes application Id
    AppId = "XXXXXXXXXX"
    endpoint = (
        "https://itunes.apple.com/AU/rss/customerreviews/id="
        + AppId
        + "/sortBy=mostRecent/json"
    )
    data = getreviews(endpoint)

    for review in data["feed"]["entry"][1:-1]:
        if not r.get(review["id"]["label"]):
            r.set(review["id"]["label"], str(int(time.time())))
            reviewcontent = review["content"]["label"]
            author = review["author"]["name"]["label"]
            rating = review["im:rating"]["label"]
            label = review["title"]["label"]
            version = review["im:version"]["label"]
            slackSend(
                SSMParameter,
                SlackWebhook,
                SlackChannel,
                SlackUsername,
                SlackEmoji,
                reviewcontent,
                author,
                rating,
                label,
                version,
            )
