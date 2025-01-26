# -*- coding: utf-8 -*-
import datetime
import os

from boltons import timeutils
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = Field()
    ACCESS_TOKEN_EXPIRE_TTL: datetime.timedelta = Field(default_factory=lambda: timeutils.parse_timedelta(os.environ.get('ACCESS_TOKEN_EXPIRE_TTL') or '30m'))
    MONGODB_URL: str = Field()
