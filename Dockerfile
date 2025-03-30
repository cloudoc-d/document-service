FROM sunpeek/poetry:py3.11-slim

COPY . /app

WORKDIR /app

RUN poetry update

CMD ["poetry", "run", "fastapi", "run", "app/main.py", "--port", "8080"]
