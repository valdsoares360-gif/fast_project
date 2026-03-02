from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fast_project.database import get_session
from fast_project.models import User
from fast_project.security import (
    get_current_user,
    get_password_hash,
)
from fast_project.squemas import (
    UserList,
    UserPublic,
    UserSquema,
)

Current_User = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_session)]
router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSquema, session: Session):

    db_user = await session.scalar(
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
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: Session,
    current_user: Current_User,
    limit: int = 10,
    offset: int = 0,
):
    stmt = select(User).offset(offset).limit(limit)
    users = (await session.scalars(stmt)).all()

    return {'user': users}


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSquema,
    session: Session,
    current_user: Current_User,
):
    target_user = await session.get(User, user_id)
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
        await session.commit()
        await session.refresh(current_user)
        return current_user

    except IntegrityError:
        raise HTTPException(
            detail='username or email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    session: Session,
    current_user: Current_User,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'user deleted'}
