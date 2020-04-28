#! /bin/bash

CONTAINER_RUN_CMD=${CONTAINER_RUN_CMD:-"docker run"}
CONTAINER_ENV_FILE=${CONTAINER_ENV_FILE:-"dev-local-env"}

${CONTAINER_RUN_CMD} \
    --rm \
    -it \
    --network="host" \
    --env-file ${CONTAINER_ENV_FILE} \
    timbot:timbot
