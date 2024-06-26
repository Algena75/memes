# API сервис хранения мемов
Реализация асинхронного сервиса с микросевисной архитектурой.
![Схема проекта](files/project_schema.png)
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* FastAPI
* PostgreSQL
* MinIO
* Asyncio
* SQLAlchemy
* Pytest
* Docker
* Nginx
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:algena75/memes.git
```

```
cd memes
```

### Запуск виртуального окружения

Создание виртуального окружения:
```bash
poetry env use python3.10
```
Установка зависимостей:
```bash
poetry install --with test,web,images
```
Запуск оболочки и активация виртуального окружения (из папки проекта):
```bash
poetry shell
```
Проверка активации виртуального окружения:
```bash
poetry env list
```
## Подготовка:
Создать в корне проекта файл `.env` (см `.env.example`) для подключения БД и контейнера MinIO.

* #### для запуска проекта в контейнерах выполнить:
    ```bash
    docker compose -f docker-compose.yml up -d
    ```
Oткрыть в браузере ` http://127.0.0.1/docs `.
Будет создано 5 контейнеров. Публичный web принимает через API файл и его описание, если файл графический, 
информация передаётся в контейнер images для обработки. Если имя файла уже существует, формируется новое имя файла.
После получения ответа от images, файл записывается в хранилище. Контейнер images работает с базой данных.
При удалении файла информация о файле удаляется из базы данных, а файл удаляется из хранилища.
Эндпоинт `/downloads/{filename}` формирует ссылку на скачивание файла из хранилища.
## Автотесты:
Написаны тесты для тестирования основной функциональности сервиса. Эндпоинты публичного сервиса проверяют
взаимодействие с приватным сервисом. Эндпоинты приватного сервиса - взаимодействие с БД.
Для запуска тестов выполнить в терминале `pytest`.
