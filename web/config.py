from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_TITLE: str = 'API для работы с коллекцией мемов'
    APP_DESCRIPTION: str = 'Тестовое задание'
    PRIVATE_URL: str = 'http://127.0.0.1:8001'
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", 'minio:9000')
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", 'my_bucket')


    class Config:
        env_file = '.env'
        extra = 'allow'


settings = Settings()

UPLOAD_TO = 'files/'
