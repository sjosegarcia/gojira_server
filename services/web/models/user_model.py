from models.base import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    username = Column(String, default=False, nullable=True)
    password = Column(String, nullable=True)
    email = Column(String, default=False, nullable=True)
    firstname = Column(String, default=False, nullable=True)
    lastname = Column(String, default=False, nullable=True)
    dob = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    last_login_date = Column(DateTime(timezone=True), nullable=True)
    photo_url = Column(String, nullable=True)
    email_verified = Column(Boolean, default=False)
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    deleted = Column(Boolean, default=False, nullable=False)
