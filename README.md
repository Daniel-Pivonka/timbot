### Purpose
A Slack "bot" to replace our dear friend Tim

##### Building the container image
```bash
$ make build-timbot
```

##### Running the timbot image locally
```bash
$ make run-timbot
```

##### Running natively
- `pip install slackclient`
- set enviorment variables for `SLACK_API_TOKEN`, `SLACK_CHANNEL_NAME`, `SLACK_TIMBOT_USER_ID`
- run `python timbot.py`

## References
- https://api.slack.com/custom-integrations/legacy-tokens
- https://slack.dev/python-slackclient/
- https://api.slack.com/methods 

