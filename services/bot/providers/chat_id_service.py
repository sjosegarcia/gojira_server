from providers.utils import is_member
from repositories.bot_repository import BotRepository
from telegram.ext import CommandHandler
from telegram import ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


class ChatIdService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository
        self._process_handlers()

    def _get_chat_id(self, update: Update, context: CallbackContext) -> None:
        user_id = update.effective_user.id
        chat = update.effective_chat
        member = chat.get_member(user_id)
        if is_member(member):
            return
        update.message.reply_text(
            f"chat_id: {chat.id + 2**32}",
            quote=False,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            CommandHandler("chatid", self._get_chat_id)
        )
