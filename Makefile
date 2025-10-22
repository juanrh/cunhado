SHELL := /bin/bash

.SILENT:

UNAME := $(shell uname)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MAIN_SRC := $(ROOT_DIR)/cunhado
VENV_DIR := $(MAIN_SRC)/.venv
PYTHON := $(VENV_DIR)/bin/python

default: help

# https://news.ycombinator.com/item?id=11939200
.PHONY: help
help:	### list main targets

ifeq ($(UNAME), Linux)
	@grep -P '^[a-zA-Z_-_/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else
	@# this is not tested, but prepared in advance for you, Mac drivers
	@awk -F ':.*###' '$$0 ~ FS {printf "%15s%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

# https://docs.astral.sh/uv/guides/projects/
# [Sync the workspace](https://docs.astral.sh/uv/concepts/projects/sync/)
# so `uv` setups the environment and make the dependencies available to your IDE
.PHONY: devenv
devenv:   ### setup developlent environment
	cd $(MAIN_SRC) && uv sync --all-extras

.PHONY: clean
clean:	### remove any compiled artifacts
	rm -rf $(VENV_DIR)

.PHONY: run
run: export LOTRBOT_ENV_FILE_PATH=$(shell echo $${LOTRBOT_ENV_FILE_PATH:-$(HOME)/.lotrbot.env})
run: export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
run:	### run the agent
	$(PYTHON) $(MAIN_SRC)/main.py 
