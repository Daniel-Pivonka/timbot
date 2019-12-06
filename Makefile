ROOT_DIR:= $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))

CONTAINER_BUILD_CMD = podman build

build-timbot:
	$(CONTAINER_BUILD_CMD) -f Dockerfile -t timbot $(ROOT_DIR)

run-timbot:
	$(ROOT_DIR)/scripts/run-timbot-local.sh
