import errno
import os
from minio import Minio


from aiohttp import ClientSession

from web.config import UPLOAD_TO


async def get_client_session():
    async with ClientSession() as client_session:
        yield client_session


async def write_file(file_name: str, contents) -> None:
    with open(f'{UPLOAD_TO}{file_name}', 'wb') as f:
        f.write(contents)


async def remove_file(file_name: str):
    try:
        os.remove(f'{UPLOAD_TO}{file_name}')
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
