# mypy: ignore-errors
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from endpoints.api_endpoints import api_router
import endpoints.bot_endpoints as bot_endpoints
from setup.config import get_settings
from models.base import Base
from containers.bot_container import BotContainer


def start_app() -> FastAPI:
    bot_container = BotContainer()
    bot_container.bot_repository()
    db = bot_container.database_service()
    bot_container.chat_repository()
    engine = db.engine
    bot_container.bot_service()
    bot_container.token_service()
    bot_container.ban_service()
    bot_container.cas_service()
    bot_container.chatid_service()
    bot_container.link_removal_service()
    bot_container.welcome_message_service()
    bot_container.scam_reporter_service()
    bot_container.track_chat_service()
    bot_container.wire(modules=[bot_endpoints])
    settings = get_settings()
    app = FastAPI(
        debug=settings.debug,
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.bot_container = bot_container
    app.include_router(api_router)
    # app.add_middleware(SessionMiddleware, secret_key=settings.api_secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown() -> None:
        pass

    return app
