from http import HTTPStatus

from fastapi import FastAPI

from fast_project.routers import auth, todos, users
from fast_project.squemas import (
    Message,
)

app = FastAPI(title='PROJECT!')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'PROJETO USANDO FASTAPI'}
