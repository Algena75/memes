FROM python:3.10-slim

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./README.md ./alembic.ini /app/

COPY ./alembic /app/alembic
COPY ./web /app/web
COPY ./images /app/images

RUN apt update && pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --with images --no-interaction --no-ansi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY ./docker/server-entrypoint.sh /app
RUN chmod +x ./server-entrypoint.sh
