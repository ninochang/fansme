import datetime
import jwt

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.google import GoogleSSO
from typing import Annotated


import src.dependencies

from . import application as app
from . import dependencies

from src import config
from src.schemas import User, Token

def create_access_token(data: dict, exp: datetime.timedelta | int = None):
    to_encode = data.copy()
    
    if isinstance(exp, int):
        exp = datetime.datetime.fromtimestamp(exp, datetime.UTC)

    exp = exp or datetime.datetime.now(datetime.UTC) + config.ACCESS_TOKEN_EXPIRE_TTL

    to_encode.update({'exp': exp})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm='HS256')
    
    return encoded_jwt


@app.post('/login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = User(id=form_data.username, username=form_data.password)
    access_token = create_access_token(
        data={'sub': user.username},
    )
    return Token(access_token=access_token, token_type='bearer')


@app.get('/me', response_model=User)
async def get_me_info(
    user: Annotated[User, Depends(src.dependencies.authenticated)],
):
    return user


@app.get('/login/google')
async def google_login(google_sso: GoogleSSO = Depends(dependencies.get_google_sso)):
    async with google_sso:
        return await google_sso.get_login_redirect()


@app.get('/login/google/callback')
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(dependencies.get_google_sso)) -> Token:
    async with google_sso:
        user = await google_sso.verify_and_process(request)
        access_token = create_access_token(
            data={'sub': user.id}
        )
    return Token(access_token=access_token, token_type='bearer')

