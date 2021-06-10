from repositories.chat_repository import ChatRepository
from repositories.bot_repository import BotRepository
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram import ParseMode


class ScamReporterService:

    _REGISTER_CHAT = 0

    def __init__(
        self, bot_repository: BotRepository, chat_repository: ChatRepository
    ) -> None:
        self.bot_repository = bot_repository
        self.chat_repository = chat_repository
        self._process_handlers()

    async def _report_user(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            "KLK",
            quote=False,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )
        chat = update.effective_chat
        chat_in_db = await self.chat_repository.get_chat(chat)
        if not chat_in_db.toggle_report_command:
            return
        message = update.effective_message
        bot = message.bot
        bot.send_message(
            chat_in_db.report_channel,
            f"{update.effective_user.username} has reported {message.reply_to_message.from_user.username} ID: {message.reply_to_message.from_user.id} Link: {message.link}",
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )

    async def _toggle_scam_reporter(
        self, update: Update, context: CallbackContext
    ) -> int:
        query = update.inline_query.query
        chat = update.effective_chat
        toggle = await self.chat_repository.toggle_report_command(chat)
        message = "The report feature has been toggled off"
        conversation = ConversationHandler.END
        if toggle:
            message = "The report feature has been toggled on"
            conversation = self._REGISTER_CHAT

        update.message.reply_text(
            f"{message}",
            quote=False,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )
        return conversation

    async def _register_report_channel(
        self, update: Update, context: CallbackContext
    ) -> int:
        chat = update.effective_chat
        report_channel = 0
        await self.chat_repository.add_report_channel(
            chat, report_channel=report_channel
        )
        update.message.reply_text(
            "The report channel has been added",
            quote=False,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )
        return ConversationHandler.END

    def _cancel(self, update: Update, context: CallbackContext) -> int:
        user = update.message.from_user
        update.message.reply_text(
            "Scam Reporter Configuration Cancelled.",
            quote=False,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
            allow_sending_without_reply=True,
        )

        return ConversationHandler.END

    def _process_handlers(self) -> None:
        self.bot_repository.updater.dispatcher.add_handler(
            CommandHandler(
                "report",
                callback=self._report_user,
                filters=Filters.reply,
                run_async=True,
            )
        )
        self.bot_repository.updater.dispatcher.add_handler(
            ConversationHandler(
                run_async=True,
                entry_points=[
                    CommandHandler(
                        "toggle_report",
                        callback=self._toggle_scam_reporter,
                        run_async=True,
                    )
                ],
                states={
                    self._REGISTER_CHAT: [
                        CommandHandler(
                            "register_report_channel",
                            callback=self._register_report_channel,
                            run_async=True,
                        )
                    ]
                },
                fallbacks=[CommandHandler("cancel", callback=self._cancel)],
            )
        )
