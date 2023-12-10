from fastapi import APIRouter
from talk.api.endpoints import chat_router, user_router

router = APIRouter(
    prefix="/talk/api",
)

router.include_router(user_router)
router.include_router(chat_router)
