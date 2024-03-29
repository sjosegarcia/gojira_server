from models.base import Base
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime


class Program(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    courses = relationship("Course", backref="program", lazy="immediate")
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )


class Course(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    program_id = Column(Integer, ForeignKey("program.id"))
    lessons = relationship("Lesson", backref="course", lazy="immediate")
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )


class Lesson(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    sections = relationship("Section", backref="lesson", lazy="immediate")
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )


class Section(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    body = Column(String, nullable=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)
    created_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_on = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow(),
        nullable=False,
    )
