# mypy: ignore-errors
from telegram.chatmember import ChatMember
from providers.database_service import DatabaseService
from telegram import Chat
from models.chat_model import ChatModel
from sqlalchemy import select


class ChatRepository:
    def __init__(self, database_service: DatabaseService) -> None:
        self.database_service = database_service

    async def add_chat(self, chat: Chat, inviter: str) -> None:
        db = await self.database_service.get_db().__anext__()
        chat_model = ChatModel(
            chat_id=chat.id,
            chat_name=chat.title,
            creator=self._get_creator(chat),
            inviter=inviter,
        )
        db.add(chat_model)
        db.commit()

    async def get_chat(self, chat: Chat) -> ChatModel:
        db = await self.database_service.get_db().__anext__()
        result = await db.execute(
            ChatModel.__table__.chat_id == chat.id and not ChatModel.__table__.deleted
        )
        return result.scalars().first()

    async def get_all_chats(self) -> list[ChatModel]:
        db = await self.database_service.get_db().__anext__()
        result = await db.execute(select(ChatModel))
        return result.scalars().all()

    async def delete_chat(self, chat: Chat) -> None:
        chat_in_db = await self.get_chat(chat)
        if not chat_in_db:
            return
        chat_in_db.deleted = True
        db = await self.database_service.get_db().__anext__()
        db.commit()

    def _get_creator(self, chat: Chat) -> ChatMember:
        administrators = chat.get_administrators()
        for admin in administrators:
            if admin.status == ChatMember.CREATOR:
                return admin
        return None

    async def add_report_channel(self, chat: Chat, report_channel: int) -> None:
        chat_in_db = await self.get_chat(chat)
        if not chat_in_db:
            return
        chat_in_db.report_channel = report_channel
        db = await self.database_service.get_db().__anext__()
        db.commit()

    async def toggle_report_command(self, chat: Chat) -> bool:
        chat_in_db = await self.get_chat(chat)
        if not chat_in_db:
            return
        chat_in_db.toggle_report_command = not chat_in_db.toggle_report_command
        db = await self.database_service.get_db().__anext__()
        db.commit()
        return chat_in_db.toggle_report_command
