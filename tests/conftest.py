from pathlib import Path

import asyncpg
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

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


async def create_database_if_not_exists():
    try:
        db_conn = await asyncpg.connect(user='postgres',
                                     password='postgres',
                                     database='template1',
                                     host='127.0.0.1')
        await db_conn.execute(f'''CREATE DATABASE test_base''')
        await db_conn.close()
    except:
        pass


async def delete_database():
    try:
        db_conn = await asyncpg.connect(user='postgres',
                                     password='postgres',
                                     database='template1',
                                     host='127.0.0.1')
        await db_conn.execute(f'''DROP DATABASE test_base WITH (FORCE)''')
        await db_conn.close()
    except:
        pass


@pytest.fixture
async def async_db_engine():
    SQLALCHEMY_DATABASE_URL = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/test_base"
    )

    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    try:
        await create_database_if_not_exists()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        print('SESSION IS CLOSED')
        await delete_database()


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    testing_session_local = async_sessionmaker(async_db_engine,
                                               expire_on_commit=False,
                                               class_=AsyncSession)
    async with testing_session_local() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture(scope='session')
async def private_client():
    async with AsyncClient(app=im_app,
                           base_url="http://127.0.0.1:8001") as client:
        yield client
