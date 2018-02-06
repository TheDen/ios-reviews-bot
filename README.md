# iOS Reviews SlackBot

A slackbot that pulls the latest iOS/iTunes review for your application and posts it to slack!

## Requirements

* `python3`
* A valid slack webhook, i.e, of the form `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`

## Running

The following variables in the script need to be set:

* `SlackChannel`: The slack channel you want the bot to post to (`@username` for DMs).
* `SlackUsername`: The username the bot will use.
* `SlackEmoji`: The emoji the slackbot will use.
* `IdFile`: The file that will store all the unique IDs of the reviews (make sure it's an **absolute** path)
* `SlackWebhook`: The Slack WebHook can be hardcoded if needed, but the environment variable `SLACKWEBHOOK` can be passed instead.

### Standalone
```export SLACKWEBHOOK=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX && iosreviews.py```

### Cron
Set up `iosreviews.py` as a `cron` job, for example,

```* * * * * /home/ubuntu/iosbot/iosreviews.py```
to run every minute

