import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from images.core.config import settings
from images.models import Mem

TEST_DATA = dict(filename="small.gif", description="any_text")


@pytest.mark.parametrize("new_mem_data", (TEST_DATA,))
@pytest.mark.anyio
async def test_post_add_mem(private_client: AsyncClient,
                            new_mem_data):
    """
    POST-запрос создаёт новую запись.
    """
    response = await private_client.post("/memes", data=new_mem_data)
    TEST_DATA['id'] = response.json().get('id')
    assert response.status_code == status.HTTP_201_CREATED
    assert new_mem_data.get('description') in response.text


@pytest.mark.anyio
async def test_get_all_mems(private_client: AsyncClient):
    """
    GET-запрос возвращает список мемов.
    """
    response = await private_client.get("/memes")
    assert response.status_code == status.HTTP_200_OK
    assert TEST_DATA.get('filename') in response.text


@pytest.mark.anyio
async def test_get_mem_by_id(private_client: AsyncClient):
    """
    GET-запрос по id возвращает мем.
    """
    response = await private_client.get(f'/memes/{TEST_DATA["id"]}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('description') == TEST_DATA["description"]


@pytest.mark.anyio
async def test_put_mem(private_client: AsyncClient):
    """
    PUT-запрос изменяет запись.
    """
    new_description = 'new_description'
    response = await private_client.put(f'/memes/{TEST_DATA["id"]}',
                                        data={'description': new_description})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('description') == new_description


@pytest.mark.anyio
async def test_delete_mem_by_id(private_client: AsyncClient):
    """
    DELETE-запрос по id удаляет мем.
    """
    response = await private_client.get(f'/memes/{TEST_DATA["id"]}')
    assert response.status_code == status.HTTP_200_OK
    await private_client.delete(f'/memes/{TEST_DATA["id"]}')
    response = await private_client.get(f'/memes/{TEST_DATA["id"]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
