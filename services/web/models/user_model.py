from models.base import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, default=False, nullable=True)
    username = Column(String, default=False, nullable=True)
    email = Column(String, default=False, nullable=True)
    firstname = Column(String, default=False, nullable=True)
    lastname = Column(String, default=False, nullable=True)
    dob = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    role = Column(String, nullable=False, default="USER")
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
