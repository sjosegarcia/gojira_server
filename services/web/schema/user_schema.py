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
    role: Optional[str]
    last_login_date: Optional[datetime]
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    email_verified: Optional[bool]
    photo_url: Optional[str]
    deleted: Optional[bool]


class UserInDB(User):
    id: int
