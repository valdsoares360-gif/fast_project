from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_project.routers import auth, users
from fast_project.squemas import (
    Message,
)

app = FastAPI(title='PROJECT!')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.get('/teste', tags=['testar'], response_class=HTMLResponse)
def teste():
    return '<h1>test ok</h1>'
