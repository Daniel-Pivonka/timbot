#! /bin/bash

set -x

ROOT_DIR=$(dirname "${BASH_SOURCE}")/..
ABS_PATH_TIMBOT_SCHEMA=$(readlink -f ${ROOT_DIR}/schema.sql)

CONTAINER_RUNTIME="${CONTAINER_RUNTIME:="podman"}"
CONTAINER_RUN_CMD="${CONTAINER_RUN_CMD:=$CONTAINER_RUNTIME run}"

echo "Pulling the mysql:8.0 container locally"
${CONTAINER_RUNTIME} pull mysql:8.0
echo "Running the mysql:8.0 container locally"
${CONTAINER_RUN_CMD} --name timbot-dev-ci \
    --rm \
    -v ${ABS_PATH_TIMBOT_SCHEMA}:/tmp/schema.sql \
    -e MYSQL_USER=testuser \
    -e MYSQL_ROOT_PASSWORD=testpass \
    -e MYSQL_PASSWORD=testpass \
    mysql:8.0
