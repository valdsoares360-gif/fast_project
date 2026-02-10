from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_project.database import get_session
from fast_project.models import User
from fast_project.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from fast_project.squemas import (
    Jwt_Token,
    Message,
    UserList,
    UserPublic,
    UserSquema,
)

app = FastAPI(title='PROJECT!')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.get('/teste', tags=['testar'], response_class=HTMLResponse)
def teste():
    return '<h1>test ok</h1>'


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSquema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    stmt = select(User).offset(offset).limit(limit)
    users = session.scalars(stmt).all()

    return {'user': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSquema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    target_user = session.get(User, user_id)
    if not target_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user

    except IntegrityError:
        raise HTTPException(
            detail='username or email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


@app.delete('/users/{user_id}')
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'user deleted'}


@app.post('/login', response_model=Jwt_Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='incorrect email or password ',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='incorrect email or password ',
        )

    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}



