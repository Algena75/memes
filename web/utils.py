import errno
import os
from minio import Minio
import io

from aiohttp import ClientSession

from web.config import settings, UPLOAD_TO

client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


async def get_client_session():
    async with ClientSession() as client_session:
        yield client_session


async def write_file(file_name: str, contents) -> None:
    if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
        client.make_bucket(settings.MINIO_BUCKET_NAME)
        print(f"Bucket '{settings.MINIO_BUCKET_NAME}' created!")
    else:
        print(f"Bucket '{settings.MINIO_BUCKET_NAME}' already exists.")
    value_as_a_stream = io.BytesIO(contents)
    client.put_object(settings.MINIO_BUCKET_NAME, file_name,
                      value_as_a_stream, length=len(contents))


async def remove_file(file_name: str):
    client.remove_object(settings.MINIO_BUCKET_NAME, file_name)


async def get_file(file_name: str, file_path: str):
    client.fget_object(settings.MINIO_BUCKET_NAME, file_name, file_path)
