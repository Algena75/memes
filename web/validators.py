from typing import Dict, Union


async def check_image(file_type: str) -> Union[Dict, None]:
    if 'image' not in file_type:
        return {"message": "Допускаются только изображения"}
