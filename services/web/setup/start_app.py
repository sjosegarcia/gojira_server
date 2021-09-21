# mypy: ignore-errors
from services.firebase_service import (
    init_sdk_with_service_account,
    remove_sdk_with_service_account,
)
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from endpoints.api_endpoints import api_router
from setup.config import get_settings
from models.base import Base
from services.database_service import db


def start_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        debug=bool(settings.debug),
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.include_router(api_router, prefix=settings.api_v1_str)
    app.add_middleware(SessionMiddleware)  # , secret_key=settings.api_secret_key
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.firebase_app = init_sdk_with_service_account()

    @app.on_event("startup")
    async def startup() -> None:
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown() -> None:
        remove_sdk_with_service_account(app.firebase_app)

    return app
