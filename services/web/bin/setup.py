from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# from data.db import engine
from data.models.base import Base
from routes.v1.endpoints.api_endpoints import api_router
from utils.config import get_settings


def setup_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        debug=settings.debug,
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.include_router(router=api_router, prefix=settings.api_v1_str)
    app.add_middleware(SessionMiddleware, secret_key=settings.api_secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def index() -> ORJSONResponse:
        return ORJSONResponse({"response": "This is the index directory!"})

    @app.on_event("startup")
    async def startup() -> None:
        pass
        # async with engine.begin() as conn:
        #    await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown() -> None:
        pass

    return app
