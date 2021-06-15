from fastapi import APIRouter
from endpoints.user.user_endpoints import users_router
from endpoints.education.program_endpoints import program_router
from endpoints.authentication.authentication_endpoints import authentication_router

api_router = APIRouter()

api_router.include_router(router=users_router, tags=["users"])
api_router.include_router(
    router=authentication_router, prefix="/authentication", tags=["authentication"]
)
api_router.include_router(router=program_router, prefix="/education", tags=["program"])
