from .model_schema import Model
from datetime import datetime
from typing import List, Optional


class Section(Model):
    title: str
    slug: str
    body: str
    likes: Optional[int]
    dislikes: Optional[int]


class Lesson(Model):
    title: str
    slug: str
    sections: list[Section]
    likes: Optional[int]
    dislikes: Optional[int]


class Course(Model):
    title: str
    slug: str
    lessons: list[Lesson]
    likes: Optional[int]
    dislikes: Optional[int]


class Program(Model):
    title: str
    slug: str
    courses: list[Course]


class SectionInDB(Model):
    id: int
    title: str
    slug: str
    body: str
    created_on: datetime
    updated_on: datetime
    likes: int
    dislikes: int


class LessonInDB(Model):
    id: int
    title: str
    slug: str
    sections: List[SectionInDB]
    created_on: datetime
    updated_on: datetime
    likes: int
    dislikes: int


class CourseInDB(Model):
    id: int
    title: str
    slug: str
    lessons: List[LessonInDB]
    created_on: datetime
    updated_on: datetime
    likes: int
    dislikes: int


class ProgramInDB(Model):
    id: int
    title: str
    slug: str
    courses: List[CourseInDB]
    created_on: datetime
    updated_on: datetime
