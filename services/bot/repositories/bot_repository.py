from setup.config import get_settings
from telegram.ext import Updater
from telegram import Bot


class BotRepository:
    def __init__(self) -> None:
        bot = Bot(get_settings().telegram_bot_api_key)
        self.updater = Updater(bot=bot, workers=1)
