from .model_schema import Model
from datetime import datetime


class Section(Model):
    id: int
    body: str
    created_on: datetime
    update_on: datetime
    likes: int
    dislikes: int


class Lesson(Model):
    id: int
    name: str
    sections: list[Section]
    created_on: datetime
    update_on: datetime
    likes: int
    dislikes: int


class Course(Model):
    id: int
    name: str
    lessons: list[Lesson]
    created_on: datetime
    update_on: datetime
    likes: int
    dislikes: int


class Program(Model):
    id: int
    name: str
    courses: list[Course]
    created_on: datetime
    update_on: datetime
