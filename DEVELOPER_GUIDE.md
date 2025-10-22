# Develop guide

## Setup

Project created with [`uv init cunhado`](https://docs.astral.sh/uv/guides/projects/)

- [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)
- Setups the environment and make the dependencies available to your IDE: `make devenv`
  - Alternatively, use `make install-dev` to install development tools only

See a virtual env for the project at `cunhado/.venv`

See [managing dependencies](https://docs.astral.sh/uv/guides/projects/#managing-dependencies).

See relevant Makefile targets with `make`

## How to run the agent

`bin/cunhado --help`. Consider adding that to your `PATH`


## Code Quality Tools

The project uses the following tools for code quality:

- **Mypy**: Static type checking
- **Ruff**: Linting and formatting

See relevant Makefile targets with `make`


### Configuration

- **Mypy**: Configured in `mypy.ini` with strict type checking
- **Ruff**: Configured in `pyproject.toml` for both linting and formatting
- **Line length**: 88 characters
- **Indentation**: 4 spaces
- **Quotes**: Single quotes
