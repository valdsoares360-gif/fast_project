from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_project.database import get_session
from fast_project.models import User
from fast_project.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from fast_project.squemas import (
    Jwt_Token,
)

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
user: Annotated[User, Depends(get_current_user)]


@router.post('/login', response_model=Jwt_Token)
async def login_for_acess_token(
    form_data: OAuth2Form,
    session: Session,
):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

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


@router.post('/refresh_token', response_model=Jwt_Token)
async def refresh_access_token(
    user: Annotated[User, Depends(get_current_user)],
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
