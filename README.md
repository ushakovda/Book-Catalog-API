## Book Catalog API

Простой REST API-сервис на Django + DRF для управления книгами и тегами, а также просмотра истории изменений книги.

## Требования

- Docker
- Docker Compose

## Запуск

1) В корне проекта выполните:
```bash
docker compose up --build
```

## Postman
Для удобства тестирования можно импортировать коллекцию запросов Postman.
Файл лежит в репозитории: `swarmica.postman_collection`

Импорт:
1) Postman → Import → File
2) выбрать `postman/book-catalog.postman_collection.json`
