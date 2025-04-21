# Documents Service

Сервис отвечает за создание, отображение и редактирование документов и описаний стилей форматирования.

## Окружения разработки
```sh
git clone https://github.com/cloudoc-d/document-service.git
cd document-service
# инициализация poetry окружения
poetry install
# запуск сервисов-зависимостей (mongodb, redis)
docker compose up -d
# запуск приложения
poetry run fastapi dev app/main.py
```

## Тестирование
```sh
# установка зависимостей
poetry install --with test
# запуск тестов
poetry run pytest
```

## CLI-инструменты приложения
```sh
# установка зависимостей
poetry install --with cli-tools
# генерация 10 документов
poetry run cli-tools 10
```
Подробнее о cli-инструментах можно узнать указав `-h` аргумент.

| Описание         | Ссылка                              |
|------------------|-------------------------------------|
| API              | [http://localhost:8080](http://localhost:8080)       |
| Документация     | [http://localhost:8080/docs](http://localhost:8080/docs) |
| MongoDB instance | [mongodb://localhost:27017](mongodb://localhost:27017) |
