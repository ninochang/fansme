# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi_sso.sso.google import GoogleSSO

from . import settings

application = router = APIRouter(
    tags=['social'],
)

from . import settings

config = settings.Settings()

from . import dependencies, endpoints

__all__ = ('endpoints', 'dependencies', )
