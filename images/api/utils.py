from pathlib import Path
from random import choices
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from images.core.config import ARRAY
from images.models import Mem


async def get_file_name(
        file_name: str,
        session: AsyncSession,
) -> Optional[str]:
    db_file = await session.execute(select(Mem).where(
        Mem.name == file_name
    ))
    if db_file.scalars().first():
        name_suffix: str = ''.join(choices(ARRAY, k=8))
        ext: str = Path(file_name).suffix
        new_name: str = f'{file_name[:-len(ext)]}_{name_suffix}{ext}'
        file_name = await get_file_name(new_name, session)
    return file_name
