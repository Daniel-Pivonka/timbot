#! /bin/bash

CONTAINER_RUNTIME="podman"
CONTAINER_RUN_CMD="${CONTAINER_RUNTIME} run"

echo "Pulling the mysql:8.0 container locally"
${CONTAINER_RUNTIME} pull mysql:8.0
echo "Running the mysql:8.0 container locally"
${CONTAINER_RUN_CMD} -d --network host -e MYSQL_ROOT_PASSWORD=testpass -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpass -e MYSQL_DATABASE=timbot mysql:8.0
