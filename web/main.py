import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from web.config import settings
from web.endpoints import router

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)
app.include_router(router)
add_pagination(app)


def run():
    """Функция программного запуска проекта для poetry."""
    uvicorn.run("web.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    run()
