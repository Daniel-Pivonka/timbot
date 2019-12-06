#! /bin/bash

set -e

if [[ -z "$SLACK_API_TOKEN" ]]; then
    echo "You need to set the \$SLACK_API_TOKEN"
    exit 1
elif [[ -z "$SLACK_CHANNEL_NAME" ]]; then
    echo "You need to set the \$SLACK_CHANNEL_NAME"
    exit 1
elif [[ -z "$SLACK_TIMBOT_USER_ID" ]]; then
    echo "You need to set the \$SLACK_TIMBOT_USER_ID"
    exit 1
fi

CONTAINER_RUN_CMD=${CONTAINER_RUN_CMD:-"podman run"}

set -x

${CONTAINER_RUN_CMD} \
    --name timbot-local \
    --rm \
    -e SLACK_API_TOKEN="${SLACK_API_TOKEN}" \
    -e SLACK_CHANNEL_NAME="${SLACK_CHANNEL_NAME}" \
    -e SLACK_TIMBOT_USER_ID="${SLACK_TIMBOT_USER_ID}" \
    -d \
    -it timbot
