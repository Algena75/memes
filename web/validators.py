from http import HTTPStatus
from typing import Dict, Union

from fastapi import HTTPException


async def check_image(file_type: str) -> Union[Dict, None]:
    if 'image' not in file_type:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Допускаются только изображения!'
        )
