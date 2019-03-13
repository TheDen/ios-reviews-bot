# iOS Reviews SlackBot

A slackbot that pulls the latest iOS/iTunes review for your application and posts it to slack!

## Requirements

* `python3`
* A valid slack webhook, i.e, of the form `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
* `boto3` + `requests` (from `requirements.txt`)
* [python-lambda-local](https://github.com/HDE/python-lambda-local)

## Running

Install the dev requirements:

```
pip3 install -r requirements-dev.txt
```

The following variables are needed in the script:

* `SlackChannel`: The slack channel you want the bot to post to (`@username` for DMs).
* `SlackUsername`: The username the bot will use.
* `SlackEmoji`: The emoji the slackbot will use.
* `SlackWebhook`: The Slack WebHook is pulled from AWS's SSM using boto3—the parameter name is set as `SSMParameter`
* `redispw`: The redis password is pulled from AWS's SSM, parameter name is assumed to be `redispw-SSMparam`

To deploy the lambda function via `python-lambda-local`

```
python3 -m venv .
. bin/activate
pip install python-lambda
pip install -r requirements.txt
lambda deploy
```
