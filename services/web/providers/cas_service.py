from schema.cas_model import CasModel
from repositories.bot_repository import BotRepository
from httpx import get, ReadTimeout
from setup.config import get_settings
from fastapi import HTTPException, status
from telegram.ext import MessageHandler, Filters
from telegram import ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


class CasService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository
        self._process_handlers()

    def _get_cas(self, user_id: int) -> CasModel:
        try:
            response = get(f"{get_settings().cas_api_url}check?user_id={user_id}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"There is an issue connecting with CAS {response.json()}",
                )
            return CasModel(**response.json())
        except ReadTimeout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is an issue connecting with CAS {response.json()}",
            )

    def _new_user(self, update: Update, context: CallbackContext) -> None:
        for member in update.message.new_chat_members:
            cas = self._get_cas(member.id)
            if cas.result:
                banned = update.message.bot.kick_chat_member(
                    update.effective_chat.id, member.id
                )
                if banned:
                    update.message.reply_text(
                        f"{member.username} has been banned by CAS.",
                        quote=False,
                        parse_mode=ParseMode.HTML,
                        disable_notification=True,
                        disable_web_page_preview=True,
                        allow_sending_without_reply=True,
                    )

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            MessageHandler(Filters.status_update.new_chat_members, self._new_user)
        )
