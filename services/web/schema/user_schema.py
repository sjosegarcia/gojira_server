from .model_schema import Model
from datetime import datetime, date
from typing import Optional


class User(Model):
    uid: Optional[str]
    username: Optional[str]
    email: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    dob: Optional[date]
    role: str
    last_login_date: Optional[datetime]
    created_on: datetime
    updated_on: datetime
    email_verified: bool
    photo_url: Optional[str]
    deleted: bool


class UserInDB(User):
    id: int
