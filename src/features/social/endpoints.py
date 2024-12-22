import datetime
import jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from . import application as app

from src import config, dependencies
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
    user: Annotated[User, Depends(dependencies.authenticated)],
):
    return user



