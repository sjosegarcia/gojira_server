from repositories.chat_repository import ChatRepository
from repositories.bot_repository import BotRepository
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.error import BadRequest
from telegram.chatmember import ChatMember
from telegram.chat import Chat
from telegram import ParseMode
from .utils import is_admin, is_member


class BanService:
    def __init__(
        self, bot_repository: BotRepository, chat_repository: ChatRepository
    ) -> None:
        self.bot_repository = bot_repository
        self.chat_repository = chat_repository
        self._process_handlers()

    def blanket_ban(self, update: Update, context: CallbackContext) -> None:
        pass

    def _unban_user_command(self, update: Update, context: CallbackContext) -> None:
        chat = update.effective_chat
        message = update.effective_message
        user_id = message.from_user.id
        member = chat.get_member(user_id)
        if is_member(member):
            return
        replied_user_id = message.reply_to_message.from_user.id
        replied_member = chat.get_member(replied_user_id)
        if is_admin(replied_member):
            update.message.reply_text(
                "You must be kidding me, you cannot unban an admin.",
                quote=False,
                parse_mode=ParseMode.HTML,
                disable_notification=True,
                disable_web_page_preview=True,
                allow_sending_without_reply=True,
            )
            return
        self._handle_unban(
            update=update,
            member=replied_member,
            chat=chat,
        )

    def _ban_user_command(self, update: Update, context: CallbackContext) -> None:
        query = update.inline_query.query if update.inline_query else None
        ban_length = 367  # perma ban
        if query:
            if query.isnumeric():
                ban_length = int(query)
        chat = update.effective_chat
        message = update.effective_message
        user_id = message.from_user.id
        member = chat.get_member(user_id)
        if is_member(member):
            return
        replied_user_id = message.reply_to_message.from_user.id
        replied_member = chat.get_member(replied_user_id)
        if is_admin(replied_member):
            update.message.reply_text(
                "You must be kidding me, you cannot ban an admin.",
                quote=False,
                parse_mode=ParseMode.HTML,
                disable_notification=True,
                disable_web_page_preview=True,
                allow_sending_without_reply=True,
            )
            return
        self._handle_ban(
            update=update,
            ban_length=ban_length,
            member=replied_member,
            chat=chat,
        )

    def _handle_ban(
        self,
        update: Update,
        ban_length: int,
        member: ChatMember,
        chat: Chat,
    ) -> bool:
        bot = update.message.bot
        banned = False
        try:
            banned = bot.kick_chat_member(
                chat.id, member.user.id, until_date=ban_length
            )
            if banned:
                update.message.reply_text(
                    f"{member.user.username} has been eviscerated from the face of the earth.",
                    quote=False,
                    parse_mode=ParseMode.HTML,
                    disable_notification=True,
                    disable_web_page_preview=True,
                    allow_sending_without_reply=True,
                )
        except BadRequest:
            update.message.reply_text(
                f"There was an issue processing your request, it might be an issue with the server or its possible that {member.user.username} is an administrator",
                quote=False,
                parse_mode=ParseMode.HTML,
                disable_notification=True,
                disable_web_page_preview=True,
                allow_sending_without_reply=True,
            )
        return banned

    def _handle_unban(
        self,
        update: Update,
        member: ChatMember,
        chat: Chat,
    ) -> bool:
        bot = update.message.bot
        unbanned = False
        try:
            unbanned = bot.unban_chat_member(
                chat.id, member.user.id, only_if_banned=True
            )
            if unbanned:
                update.message.reply_text(
                    f"{member.user.username} was allowed into the cookie jar!",
                    quote=False,
                    parse_mode=ParseMode.HTML,
                    disable_notification=True,
                    disable_web_page_preview=True,
                    allow_sending_without_reply=True,
                )
        except BadRequest:
            update.message.reply_text(
                f"There was an issue processing your request. The user in question: {member.user.username}",
                quote=False,
                parse_mode=ParseMode.HTML,
                disable_notification=True,
                disable_web_page_preview=True,
                allow_sending_without_reply=True,
            )
        return unbanned

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            CommandHandler(
                "ban", filters=Filters.reply, callback=self._ban_user_command
            )
        )
        self.bot_repository.updater.dispatcher.add_handler(
            CommandHandler(
                "unban", filters=Filters.reply, callback=self._unban_user_command
            )
        )
