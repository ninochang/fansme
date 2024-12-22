from fastapi import Request, HTTPException, Body
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.base import SSOBase, OpenID
from . import config

class PasswordSSO(SSOBase):
    provider = 'password'

    async def verify_and_process(self, username: str, password: str):
        # GET user by username from db
        user = {
            'id': 'dummy_id',
            'username': username, 
            'password': '1234',
        }
        if password != user['password']:
            raise HTTPException(status_code=403)

        return user

def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        config.SSO_GOOGLE_CLIENT_ID, 
        config.SSO_GOOGLE_CLIENT_SECRET, 
        config.SSO_GOOGLE_CALLBACK_URL,
    )

def get_password_sso() -> PasswordSSO:
    return PasswordSSO(
        client_id=None,
        client_secret=None,
    )
