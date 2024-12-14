from fastapi import APIRouter
from fastapi_sso.sso.google import GoogleSSO

from . import settings

application = router = APIRouter(
    tags=['social'],
)

from . import settings
config = settings.Settings()

from . import endpoints, dependencies

__all__ = ('endpoints', 'dependencies', )


