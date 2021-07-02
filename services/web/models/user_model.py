from models.base import Base
from datetime import datetime
from sqlalchemy import Column, String, DateTime, BigInteger, Boolean


class User(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(String, nullable=True)
    username = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=True, unique=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    dob = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    last_login_date = Column(DateTime(timezone=True), nullable=True)
    photo_url = Column(String, nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)
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
