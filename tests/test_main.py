import pytest
from fastapi import status
from httpx import AsyncClient

from tests.conftest import MOCK_RESPONSE


@pytest.mark.anyio
async def test_get_memes(client: AsyncClient):
    """
    Проверка эндпоинта /memes с get-запросом. Localhost:8001 не отвечает.
    """
    response = await client.get("/memes")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.anyio
async def test_get_memes_id_mock(client: AsyncClient, mock_response):
    """
    Проверка эндпоинта /memes/{id} с get-запросом.
    """
    response = client.get("/memes/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == MOCK_RESPONSE


@pytest.mark.anyio
async def test_get_memes_id(client: AsyncClient):
    """
    Проверка эндпоинта /memes/{id} с get-запросом. Localhost:8001 не отвечает.
    """
    response = await client.get("/memes/1")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.anyio
async def test_post_memes_txt_file(client: AsyncClient):
    """
    Проверка эндпоинта /memes с post-запросом текстового файла.
    """
    with open("tests/post/text_file.txt", "rb") as text_file:
        files = {'file': text_file}
        response = await client.post("/memes", files=files)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Допускаются только изображения!'}


@pytest.mark.anyio
async def test_post_memes_image_file(client: AsyncClient):
    """
    Проверка эндпоинта /memes с post-запросом изображения.
    Localhost:8001 не отвечает.
    """
    with open("tests/post/image.jpg", "rb") as image_file:
        files = {'file': image_file}
        response = await client.post("/memes", files=files)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {'detail': 'Сервис недоступен.'}


@pytest.mark.anyio
async def test_put_memes(client: AsyncClient):
    """
    Проверка эндпоинта /memes/{id} с put-запросом. Localhost:8001 не отвечает.
    """
    response = await client.put("/memes/1", data={'description': 'any'})
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {'detail': 'Сервис недоступен.'}
