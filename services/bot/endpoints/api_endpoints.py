from fastapi import APIRouter
from .bot_endpoints import telegram_bot_router

api_router = APIRouter()
api_router.include_router(router=telegram_bot_router, tags=["telegram_bot"])
