# Documents Service

Сервис отвечает за создание, отображение и редактирование документов и описаний стилей форматирования.

## Окружения разработки
```sh
git clone https://github.com/cloudoc-d/document-service.git
cd document-service
docker network cloudoc_network
docker compose up
# исполнение тестов
docker exec ds-app poetry run pytest
```

| Описание         | Ссылка                              |
|------------------|-------------------------------------|
| API              | [http://localhost:8080](http://localhost:8080)       |
| Документация     | [http://localhost:8080/docs](http://localhost:8080/docs) |
| MongoDB instance | [mongodb://localhost:27017](mongodb://localhost:27017) |
