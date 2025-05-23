# User chat

## Development

### Dependencies

The project manager used is [Poetry](https://python-poetry.org/) (version `>=2.0.0`).
It has to be installed and used in order to correctly add dependencies to the project.

Python `^3.11` is required. Install using [`pyenv`](https://github.com/pyenv/pyenv) (don't forget about [build dependencies](https://github.com/pyenv/pyenv)!):

```shell
pyenv install 3.11
```

Install the project in a local virtual environment:
```shell
PYENV_VERSION=3.11 python3 -m venv .venv
VIRTUAL_ENV=.venv poetry install --with dev
```

### Build

```shell
# production environment
docker build -t user-chat:latest --target=prod .

# development environemnt (includes pytest, ruff, mypy and hot-reload)
docker build -t user-chat:dev --target=dev .
```

### Development

# Dev variables defined in .env in dev-ops repo


#### Running the app

Run locally:

```shell
poetry run uvicorn --reload user_chat.app.main:app --port 8080
 ```

Run the dev image with hot reload:

```shell
docker run -it --env-file=.env \
    --mount type=bind,src=$(pwd)/user_chat,dst=/app/user_chat \
    user_chat:dev
```

Run the prod image:

```shell
docker run -it --env-file=.env user_chat:latest
```

#### Contributing

```shell
poetry run pre-commit install
```

or run checks manually:

```shell
# verify pyproject.toml integrity
poetry check
# run tests
poetry run pytest
# run ruff check
poetry run ruff check [--fix]
# run mypy
poetry run mypy .
# reformat code
poetry run ruff format
```
