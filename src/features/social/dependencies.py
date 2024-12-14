from fastapi_sso.sso.google import GoogleSSO
from . import config

def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        config.SSO_GOOGLE_CLIENT_ID, 
        config.SSO_GOOGLE_CLIENT_SECRET, 
        config.SSO_GOOGLE_CALLBACK_URL,
    )
