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
elif [[ -z "$SQL_HOST" ]]; then
    echo "You need to set the \$SQL_HOST"
    exit 1
elif [[ -z "$SQL_USER" ]]; then
    echo "You need to set the \$SQL_USER"
    exit 1
elif [[ -z "$SQL_PASSWORD" ]]; then
    echo "You need to set the \$SQL_PASSWORD"
    exit 1
elif [[ -z "$SQL_DATABASE" ]]; then
    echo "You need to set the \$SQL_DATABASE"
    exit 1
fi

CONTAINER_RUN_CMD=${CONTAINER_RUN_CMD:-"docker run"}

set -x

${CONTAINER_RUN_CMD} \
    --name timbot-local \
    --restart always \
    --network="host" \
    -e SLACK_API_TOKEN="${SLACK_API_TOKEN}" \
    -e SLACK_CHANNEL_NAME="${SLACK_CHANNEL_NAME}" \
    -e SLACK_TIMBOT_USER_ID="${SLACK_TIMBOT_USER_ID}" \
    -e MYSQL_USER="$MYSQL_USER" \
    -e MYSQL_PASSWORD="$MYSQL_PASSWORD" \
    -e MYSQL_HOST="$MYSQL_HOST" \
    -e MYSQL_DATABASE="$MYSQL_DATABASE" \
    -d \
    -it timbot
