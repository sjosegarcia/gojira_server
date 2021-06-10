from fastapi import APIRouter
from endpoints.user.user_endpoints import users_router

api_router = APIRouter()

api_router.include_router(router=users_router, tags=["users"])
