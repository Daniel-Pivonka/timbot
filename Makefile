SHELL := /bin/bash

ROOT_DIR:= $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))

CONTAINER_BASE_CMD := docker
CONTAINER_BUILD_CMD := $(CONTAINER_BASE_CMD) build
CONTAINER_RUN_IN_BG := true

TIMBOT_IMAGE_NAME := timbot-local

build:
	$(CONTAINER_BUILD_CMD) -f Dockerfile -t timbot:timbot $(ROOT_DIR)

run:
	$(ROOT_DIR)/scripts/run-timbot-local.sh

dev:
	$(ROOT_DIR)/scripts/run-timbot-dev.sh

stop:
	$(CONTAINER_BASE_CMD) stop $(TIMBOT_IMAGE_NAME)

clean:
	$(MAKE) stop-timbot
	$(CONTAINER_BASE_CMD) rm $(TIMBOT_IMAGE_NAME)
