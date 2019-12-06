# timbot
A Slack "bot" to replace our dear friend Tim

## Usage
### Normal Run 
TODO

### Local Run
- `$ pip install slackclient`
- Set enviorment variables for `SLACK_API_TOKEN`, `SLACK_CHANNEL_NAME`, `SLACK_TIMBOT_USER_ID`
- Run `$ python timbot.py`

### Local Run with Containers
As an advanced piece of software, timbot features container support via Docker

##### Building the container image
```bash
$ make build-timbot
```

##### Running the timbot image locally
```bash
$ make run-timbot
```

## References
- https://api.slack.com/custom-integrations/legacy-tokens
- https://slack.dev/python-slackclient/
- https://api.slack.com/methods 
