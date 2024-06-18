FROM python:3.10-slim

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./README.md ./alembic.ini /app/

RUN apt update -y && apt upgrade -y
RUN pip install poetry==1.7.0

# RUN poetry cache clear --all pypi
RUN poetry install --no-interaction --no-ansi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./alembic /app/alembic
COPY ./web /app/web
COPY ./images /app/images

CMD ["poetry", "run", "images"]
