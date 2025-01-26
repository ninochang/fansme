import jwt

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from src import config
from src.schemas import User as UserSchema
from src.models import User

# OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def authenticated(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate": "Bearer'},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        if not (user_id := payload.get('sub')):
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    if not (user := User.objects.filter(id=user_id).only('username').first()):
        raise HTTPException(status_code=401)

    return UserSchema(id=str(user.id), username=user.username)
