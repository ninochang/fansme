import datetime
import jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from . import application as app

from src import config, dependencies
from src.schemas import User, Token

def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm='HS256')
    return encoded_jwt


@app.post('/login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = User(id=form_data.username, username=form_data.password)
    access_token_expires = config.ACCESS_TOKEN_EXPIRE_TTL
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@app.get('/me', response_model=User)
async def get_me_info(
    user: Annotated[User, Depends(dependencies.authenticated)],
):
    return user



