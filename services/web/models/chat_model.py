from sqlalchemy.sql.sqltypes import Boolean
from models.base import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class ChatModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    chat_id = Column(NUMERIC, nullable=False)
    chat_name = Column(String, nullable=False)
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    creator = Column(String, nullable=False)
    inviter = Column(String, nullable=False)
    welcome_message = Column(String, nullable=True)
    report_channel = Column(NUMERIC, nullable=True)
    toggle_report_command = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, default=False, nullable=False)
