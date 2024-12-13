from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
