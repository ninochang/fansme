# -*- coding: utf-8 -*-
from pydantic import BaseModel


class LoginUserPassword(BaseModel):
    username: str
    password: str
