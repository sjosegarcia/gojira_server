from .model_schema import Model
from datetime import datetime, date
from typing import Optional


class User(Model):
    uid: str
    username: Optional[str]
    email: str
    firstname: str
    lastname: str
    dob: Optional[date]
    is_active: bool
    last_login_date: Optional[datetime]
    created_on: datetime
    updated_on: datetime
    email_verified: bool
    photo_url: Optional[str]


class UserInDB(User):
    id: int
