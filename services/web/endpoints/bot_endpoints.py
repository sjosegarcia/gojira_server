from fastapi import APIRouter
from telegram import Update
from fastapi.requests import Request
from setup.config import get_settings
from fastapi.responses import ORJSONResponse
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from containers.bot_container import BotContainer, BotService, BotRepository
from loguru import logger

telegram_bot_router = APIRouter()


@telegram_bot_router.get(f"/{get_settings().telegram_bot_api_key}/setwebhook")
@inject
async def bot_webhook(
    bot_service: BotService = Depends(Provide[BotContainer.bot_service]),
) -> ORJSONResponse:
    return ORJSONResponse({"hooked": bot_service.set_webhook()})


@telegram_bot_router.get(f"/{get_settings().telegram_bot_api_key}/webhookinfo")
@inject
async def bot_webhook_info(
    bot_repository: BotRepository = Depends(Provide[BotContainer.bot_repository]),
) -> ORJSONResponse:
    return ORJSONResponse(bot_repository.updater.bot.get_webhook_info().to_dict())


@telegram_bot_router.post(f"/{get_settings().telegram_bot_api_key}")
@inject
async def bot_index(
    request: Request,
    bot_repository: BotRepository = Depends(Provide[BotContainer.bot_repository]),
) -> None:
    data = await request.json()
    logger.info(f"{data}")
    bot_repository.updater.dispatcher.process_update(
        Update.de_json(data, bot_repository.updater.dispatcher.bot)
    )
