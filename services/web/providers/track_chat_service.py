from repositories.chat_repository import ChatRepository
from repositories.bot_repository import BotRepository
from telegram.ext import ChatMemberHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram import Chat
from .utils import extract_status_change


class TrackChatService:
    def __init__(
        self, bot_repository: BotRepository, chat_repository: ChatRepository
    ) -> None:
        self.bot_repository = bot_repository
        self.chat_repository = chat_repository
        self._process_handlers()

    async def _track_chat(self, update: Update, context: CallbackContext) -> None:
        result = extract_status_change(update.my_chat_member)
        if result is None:
            return
        was_member, is_member = result

        # Let's check who is responsible for the change
        cause_name = update.effective_user.full_name

        # Handle chat types differently:
        chat = update.effective_chat
        if chat.type == Chat.PRIVATE:
            if not was_member and is_member:
                await self.chat_repository.add_chat(chat, cause_name)
            elif was_member and not is_member:
                await self.chat_repository.delete_chat(chat)
        elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            if not was_member and is_member:
                await self.chat_repository.add_chat(chat, cause_name)
            elif was_member and not is_member:
                await self.chat_repository.delete_chat(chat)
        else:
            if not was_member and is_member:
                await self.chat_repository.add_chat(chat, cause_name)
            elif was_member and not is_member:
                await self.chat_repository.delete_chat(chat)

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            ChatMemberHandler(
                self._track_chat, ChatMemberHandler.MY_CHAT_MEMBER, run_async=True
            )
        )
