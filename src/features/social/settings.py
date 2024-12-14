from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SSO_GOOGLE_CLIENT_ID: str = Field('436053855190-lsps2nrlc5383n6ks8ri8hj1kfflrljt.apps.googleusercontent.com')
    SSO_GOOGLE_CLIENT_SECRET: str = Field('SSO_GOOGLE_CLIENT_SECRET')
    SSO_GOOGLE_CALLBACK_URL: str = Field('http://localhost:8000/login/google/callback')

config = Settings()
