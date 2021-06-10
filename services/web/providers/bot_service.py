from repositories.bot_repository import BotRepository
from setup.config import get_settings


class BotService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository

    def _start_local_testing(self) -> None:
        self.bot_repository.updater.start_polling()
        self.bot_repository.updater.idle()

    def set_webhook(self) -> bool:
        hooked = self.bot_repository.updater.bot.set_webhook(
            url=f"{get_settings().telegram_bot_webhook_url}/{get_settings().telegram_bot_api_key}",
        )
        return hooked
