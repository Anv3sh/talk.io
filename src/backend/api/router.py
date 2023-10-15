from fastapi import APIRouter
from .endpoints import sahyog_router

router = APIRouter(
    prefix="/talk/api",
)

router.include_router(sahyog_router)