from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

authentication_router = APIRouter()


@authentication_router.post("/token")
async def access_token(id_token: str) -> ORJSONResponse:
    return ORJSONResponse({"id_token": id_token, "token_type": "bearer"})
