from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_project.squemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSquema,
)

app = FastAPI(title='PROJECT!')

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.get('/teste', tags=['testar'], response_class=HTMLResponse)
def teste():
    return '<h1>test ok</h1>'


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSquema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'user': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSquema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='rapaz, achei não...'
        )

    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='rapaz, achei não...'
        )

    return database.pop(user_id - 1)
