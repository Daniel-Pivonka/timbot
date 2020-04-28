# timbot

![](https://github.com/Daniel-Pivonka/timbot/workflows/flake8/badge.svg)
![](https://github.com/Daniel-Pivonka/timbot/workflows/docker/badge.svg)

A Slack "bot" to replace our dear friend Tim

## Usage

Timbot supports two methods for deploying the bot locally: run the script directly, or build and run a container.

### Prerequisites

In order to use timbot, you first need to clone the repository:

```bash
git clone https://github.com/Daniel-Pivonka/timbot/
```

And appropriately set the following environment variables:

- `$SLACK_API_TOKEN`: the legacy api slack token granted to your slack account.
- `$SLACK_CHANNEL_ID`: the channel ID number.
- `$SLACK_TIMBOT_USER_ID`: the timbot slack user ID.

### Local Run without Containers

To run timbot without using container technology, run the following commands:

- `$ pip install -r requirements.txt`
- `$ python timbot.py`

### Local Run with Containers

As an advanced piece of software, timbot features container support via your choice of container engine.

#### Building the container image

```bash
make build
```

#### Running the timbot image locally

Run the following command to run the timbot client in the foreground:

```bash
make start
```

In the case where you want to run timbot is developer-friendly environment:

```bash
make dev
```

In the case where you need to stop running the timbot image, run the following:

```bash
make stop
```

## References

- https://api.slack.com/custom-integrations/legacy-tokens
- https://slack.dev/python-slackclient/
- https://api.slack.com/methods
