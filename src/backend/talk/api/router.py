from fastapi import APIRouter
from talk.api.endpoints import user_router

router = APIRouter(
    prefix="/talk/api",
)

router.include_router(user_router)