from providers.utils import is_admin
from repositories.bot_repository import BotRepository
from telegram.ext import MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from urlextract import URLExtract
from urllib.parse import urlparse


class LinkRemovalService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository
        self.extractor = URLExtract()
        self._process_handlers()

    def _link_removal(self, update: Update, context: CallbackContext) -> None:
        if update.effective_user.is_bot:
            return
        user_id = update.effective_user.id
        chat = update.effective_chat
        member = chat.get_member(user_id)
        if is_admin(member):
            return
        message = update.effective_message
        urls = self.extractor.find_urls(message.text)
        for url in urls:
            parsed = urlparse(url)
            if "t.me" in parsed[1]:
                message.delete()

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self._link_removal)
        )
