FROM sunpeek/poetry:py3.11-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

EXPOSE 8080

RUN mkdir /app
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

CMD ["poetry", "run", "fastapi", "dev", "app/main.py", "--port", "8080", "--host", "0.0.0.0"]
