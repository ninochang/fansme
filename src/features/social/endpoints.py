# -*- coding: utf-8 -*-
import datetime
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi_sso.sso.google import GoogleSSO

import src.dependencies
from src import config
from src.schemas import Token, User

from . import application as app
from . import dependencies, schemas


def create_access_token(data: dict, exp: datetime.timedelta | int = None):
    to_encode = data.copy()

    if isinstance(exp, int):
        exp = datetime.datetime.fromtimestamp(exp, datetime.UTC)

    exp = exp or datetime.datetime.now(datetime.UTC) + config.ACCESS_TOKEN_EXPIRE_TTL

    to_encode.update({'exp': exp})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm='HS256')

    return encoded_jwt


@app.get('/me', response_model=User)
async def get_me_info(
    user: Annotated[User, Depends(src.dependencies.authenticated)],
):
    return user


@app.get('/login/google')
async def google_login(google_sso: GoogleSSO = Depends(dependencies.get_google_sso)):
    async with google_sso:
        return await google_sso.get_login_redirect()


@app.post('/login/password')
async def password_login(
    login_user: schemas.LoginUserPassword,
    password_sso: dependencies.PasswordSSO = Depends(dependencies.get_password_sso),
) -> Token:
    async with password_sso:
        user = await password_sso.verify_and_process(
            login_user.username,
            login_user.password,
        )

        access_token = create_access_token(
            data={'sub': str(user.id)}
        )
        return Token(access_token=access_token, token_type='bearer')


@app.get('/login/google/callback')
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(dependencies.get_google_sso)) -> Token:
    async with google_sso:
        user = await google_sso.verify_and_process(request)
        access_token = create_access_token(
            data={'sub': user.id}
        )
    return Token(access_token=access_token, token_type='bearer')



@app.post('/register/password')
async def password_register(
    login_user: schemas.LoginUserPassword,
    password_sso: dependencies.PasswordSSO = Depends(dependencies.get_password_sso),
) -> Token:
    async with password_sso:
        user = await password_sso.verify_and_register(
            login_user.username,
            login_user.password,
        )

        access_token = create_access_token(
            data={'sub': str(user.id)}
        )
        return Token(access_token=access_token, token_type='bearer')
