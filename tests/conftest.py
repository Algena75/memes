from pathlib import Path

import pytest
from httpx import AsyncClient

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
MOCK_RESPONSE = dict(id=1, filename='small.gif', uploaded_at='01/01/2024',
                     description='test_description')


class MockResponse:
    def __init__(self, code: int = 200) -> None:
        self.status_code = code

    @staticmethod
    def json():
        return MOCK_RESPONSE


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=w_app,
                           base_url="http://localhost") as client:
        yield client


@pytest.fixture
def mock_response(client, monkeypatch):
    """Фикстура изменяющая поведение `client.get()`"""
    def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(client, "get", mock_get)


@pytest.fixture
def mock_response_post(client, monkeypatch):
    """Фикстура изменяющая поведение `client.post()`"""
    def mock_get(*args, **kwargs):
        return MockResponse(code=201)
    monkeypatch.setattr(client, "post", mock_get)
