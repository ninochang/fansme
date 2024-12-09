from fastapi import APIRouter

application = router = APIRouter(
    tags=['auth'],
)

from . import endpoints

__all__ = ('endpoints', )
