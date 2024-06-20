import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web.config import settings
from images.models import Mem

TEST_USER = dict(email="anyuser@example.com",
                 password="anyuserpassword",
                 salary=50000)


@pytest.mark.anyio
async def test_get_memes(client: AsyncClient):
    """
    Проверка эндпоинта /memes с get-запросом.
    """
    response = await client.get("/memes")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_memes_id(client: AsyncClient):
    """
    Проверка эндпоинта /memes/{id} с get-запросом.
    """
    response = await client.get("/memes/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
