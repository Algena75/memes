import uvicorn
from fastapi import FastAPI

from images.api.endpoints import router

app = FastAPI(openapi_url=None, redoc_url=None)

app.include_router(router)


def run():
    """Функция программного запуска проекта для poetry."""
    uvicorn.run("images.main:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == '__main__':
    run()
