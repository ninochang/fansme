from fastapi import APIRouter

application = router = APIRouter(
    tags=['social'],
)

from . import endpoints

__all__ = ('endpoints', )
