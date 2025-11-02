SHELL := /bin/bash

.SILENT:

UNAME := $(shell uname)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MAIN_SRC := $(ROOT_DIR)/src/cunhado
VENV_DIR := $(ROOT_DIR)/.venv
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
	uv sync --all-extras

.PHONY: install-dev
install-dev:	### install development dependencies
	uv sync --extra dev

.PHONY: clean
clean: clean/typecheck	### remove any compiled artifacts
	rm -rf $(VENV_DIR)

.PHONY: release
release: devenv checks

.PHONY: checks
checks: typecheck lint format test	### run all checks (linters, tests, etc)
checks:
	echo
	echo "All checks passing"

.PHONY: lint
lint:	### run ruff linting
	echo
	echo "Running ruff linter ..."
	uv run ruff check $(MAIN_SRC)

.PHONY: format
format:	### run ruff formatting
	echo
	echo "Running formatting checks ..."
	uv run ruff format $(MAIN_SRC)

.PHONY: typecheck
typecheck:	### run mypy type checking
	echo
	echo "Running type checking ..."
	uv run mypy --config-file $(ROOT_DIR)/pyproject.toml .

.PHONY: clean/typecheck
clean/typecheck:
	rm -rf $(MAIN_SRC)/.mypy_cache


.PHONY: lint/fix
lint/fix:	### auto-fix linting and formatting issues
	uv run ruff check --fix $(MAIN_SRC) && uv run ruff format $(MAIN_SRC)

.PHONY: test
test:	### run all tests
	echo
	echo "Running tests ..."
	uv run pytest --pyargs tests

