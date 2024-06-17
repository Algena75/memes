from http import HTTPStatus
from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from images.api.utils import get_file_name
from images.core.db import get_async_session
from images.crud import mem_crud
from images.models import Mem

router = APIRouter()


@router.get('/memes')
async def get_memes_list(
    session: AsyncSession = Depends(get_async_session)
) -> List[Dict]:
    """Возвращает список мемов."""
    all_memes = await mem_crud.get_multi(session)
    return all_memes


@router.get('/memes/{id}')
async def get_mem(id: int,
                  session: AsyncSession = Depends(get_async_session)) -> Dict:
    """Возвращает выбранный мем."""
    mem = await mem_crud.get(id, session)
    if mem:
        return mem.dict()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Мем не найден!'
        )


@router.post('/memes')
async def create_mem(
    filename: Annotated[str, Form()], description: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session)
) -> Dict:
    """Создаёт новый мем."""
    filename = await get_file_name(filename, session)
    mem = await mem_crud.create(Mem(name=filename, description=description),
                                session)
    return mem.dict()


@router.put('/memes/{id}')
async def update_mem(
    id: int,
    filename: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    session: AsyncSession = Depends(get_async_session)
) -> Dict:
    """Обновляет ранее созданный мем."""
    mem_to_change = await mem_crud.get(obj_in=id, session=session)
    if mem_to_change:
        file_to_erase = mem_to_change.name if filename else None
        obj_in = dict()
        if filename:
            filename = await get_file_name(filename, session)
            obj_in.update(name=filename)
        if description:
            obj_in.update(description=description)
        mem = await mem_crud.update(
            mem_to_change, Mem(**obj_in), session
        )
        mem = mem.dict()
        mem['file_to_erase'] = file_to_erase
        return mem
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Мем не найден!'
        )


@router.delete('/memes/{id}')
async def delete_mem(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Dict:
    """Удаляет ранее созданный мем."""
    mem_to_delete = await mem_crud.get(obj_in=id, session=session)
    if mem_to_delete:
        file_to_erase = mem_to_delete.name
        await mem_crud.remove(db_obj=mem_to_delete, session=session)
        return dict(file_to_erase=file_to_erase)
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Мем не найден!'
        )
