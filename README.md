# timbot
A Slack "bot" to replace our dear friend Tim

## Usage
### Normal Run
TODO

### Local Run
- `$ pip install slackclient`
- Set enviorment variables for `SLACK_API_TOKEN`, `SLACK_CHANNEL_NAME`, `SLACK_TIMBOT_USER_ID`
- Run `$ python timbot.py`

#### Packages

To install packages run:

`$ pip install -r requirements.txt`

### Local Run with Containers
As an advanced piece of software, timbot features container support via Docker

##### Building the container image
```bash
$ make build-timbot
```

##### Running the timbot image locally
**Note**: Before running the following, ensure that the following environment variables are appropriately set:
- `$SLACK_API_TOKEN`: the legacy api slack token granted to your slack account.
- `$SLACK_CHANNEL_ID`: the channel ID number.
- `$SLACK_TIMBOT_USER_ID`: the timbot slack user ID.

Once those variables are set, run the following to run the timbot client in the foreground:

```bash
$ make run-timbot
```



## References
- https://api.slack.com/custom-integrations/legacy-tokens
- https://slack.dev/python-slackclient/
- https://api.slack.com/methods
