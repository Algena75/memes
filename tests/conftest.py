from pathlib import Path

import pytest
from httpx import AsyncClient

from images.core.config import settings

try:
    from images.main import app as im_app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения images `app`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `images.main`.',
    )

try:
    from web.main import app as w_app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения web `app`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `web.main`.',
    )

try:
    from images.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
        'Проверьте и поправьте: они должны быть доступны в модуле '
        '`images.core.db`.',
    )


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=w_app,
                           base_url="http://localhost") as client:
        yield client
