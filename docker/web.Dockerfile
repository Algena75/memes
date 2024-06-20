FROM python:3.10-slim

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./README.md /app/

COPY ./web /app/web
COPY ./images /app/images

RUN apt update && pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --without test --no-interaction --no-ansi

# RUN poetry cache clear --all pypi
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["poetry", "run", "web"]
