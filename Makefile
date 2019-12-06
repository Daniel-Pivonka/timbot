SHELL := /bin/bash

ROOT_DIR:= $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))

CONTAINER_BUILD_CMD := podman build
CONTAINER_RUN_IN_BG := true

build-timbot:
	$(CONTAINER_BUILD_CMD) -f Dockerfile -t timbot $(ROOT_DIR)

run-timbot:
	$(ROOT_DIR)/scripts/run-timbot-local.sh

run-timbot-bg:
	export CONTAINER_RUN_IN_BG = true

run-timbot-bg:
	$(MAKE) run-timbot
