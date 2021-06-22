from fastapi import APIRouter
from endpoints.user.user_endpoints import users_router
from endpoints.education.education_endpoints import education_router

api_router = APIRouter()

api_router.include_router(router=users_router, prefix="/user", tags=["users"])
api_router.include_router(
    router=education_router, prefix="/education", tags=["program"]
)
