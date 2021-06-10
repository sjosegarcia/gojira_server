from providers.utils import is_member
from repositories.bot_repository import BotRepository
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext import MessageHandler, Filters


class WelcomeMessageService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository
        self._process_handlers()

    def new_member(self, update: Update, context: CallbackContext) -> None:
        for member in update.message.new_chat_members:
            if not member.is_bot:
                update.message.reply_text("Welcome to GodZilliqa DeFi,")

    def _set_welcome_message(self, update: Update, context: CallbackContext) -> None:
        user_id = update.effective_user.id
        member = update.effective_chat.get_member(user_id)
        if is_member(member):
            return
        # Not done!

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            MessageHandler(Filters.status_update.new_chat_members, self.new_member)
        )
