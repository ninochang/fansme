import os
import datetime

from pydantic_settings import BaseSettings
from pydantic import Field
from boltons import timeutils

class Settings(BaseSettings):
    SECRET_KEY: str = Field()
    ACCESS_TOKEN_EXPIRE_TTL: datetime.timedelta = Field(default_factory=lambda: timeutils.parse_timedelta(os.environ.get('ACCESS_TOKEN_EXPIRE_TTL') or '30m'))
    MONGODB_URL: str = Field()
