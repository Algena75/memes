from http import HTTPStatus
from typing import Annotated, Dict, List

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from web.config import settings
from web.schemas import MemDB
from web.utils import get_client_session, get_file, remove_file, write_file
from web.validators import check_image

router = APIRouter(tags=['memes'])


@router.get('/memes', response_model=list[MemDB])
async def get_memes_list(
    session: ClientSession = Depends(get_client_session)
) -> List[MemDB]:
    """Возвращает список мемов."""
    async with session.get(f'{settings.PRIVATE_URL}/memes', ssl=False) as resp:
        return await resp.json()


@router.get('/memes/{id}', response_model=MemDB)
async def get_mem(
    id: int,
    session: ClientSession = Depends(get_client_session)
) -> Dict:
    """Возвращает выбранный мем."""
    async with session.get(f'{settings.PRIVATE_URL}/memes/{id}') as resp:
        response = await resp.json()
        if not response.get('detail'):
            return response
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=response.get('detail')
            )


@router.post('/memes', response_model=MemDB)
async def create_mem(
    file: UploadFile,
    description: Annotated[str, Form()] = None,
    session: ClientSession = Depends(get_client_session)
) -> Dict:
    """Создаёт новый мем."""
    await check_image(file.content_type)
    contents = await file.read()
    async with session.post(
        f'{settings.PRIVATE_URL}/memes/',
        data={'filename': file.filename, 'description': description}
    ) as resp:
        mem_details = await resp.json()
    await write_file(mem_details.get("name"), contents)
    return mem_details


@router.put('/memes/{id}', response_model=MemDB)
async def update_mem(
    id: int,
    file: UploadFile = None,
    description: Annotated[str, Form()] = None,
    session: ClientSession = Depends(get_client_session)
) -> Dict:
    """Обновляет ранее созданный мем."""
    if not file and not description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нет данных для изменения!'
        )
    data = dict()
    if file:
        await check_image(file.content_type)
        data.update(filename=file.filename)
        contents = await file.read()
    if description:
        data.update(description=description)
    async with session.put(
        f'{settings.PRIVATE_URL}/memes/{id}', data=data
    ) as resp:
        mem_details = await resp.json()
    if not mem_details.get('detail'):
        if file and (file_to_erase := mem_details.pop('file_to_erase')):
            await remove_file(file_to_erase)
            await write_file(mem_details.get("name"), contents)
        return mem_details
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=mem_details.get('detail')
        )


@router.delete('/memes/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_mem(
    id: int,
    session: ClientSession = Depends(get_client_session)
) -> None:
    """Удаляет ранее созданный мем."""
    async with session.delete(
        f'{settings.PRIVATE_URL}/memes/{id}'
    ) as resp:
        mem_details = await resp.json()
    if (file_to_erase := mem_details.get('file_to_erase')) is not None:
        await remove_file(file_to_erase)
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Мем не найден!'
        )


@router.get('/downloadfile/{filename}', response_class=FileResponse)
async def download_file(filename: str):
    file_path = f"./{filename}"
    await get_file(filename, file_path)
    return FileResponse(file_path, filename=filename)
