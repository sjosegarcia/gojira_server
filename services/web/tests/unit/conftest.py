from schema.education_schema import (
    Program,
    Course,
    Lesson,
    Section,
    ProgramInDB,
    CourseInDB,
    LessonInDB,
    SectionInDB,
)
from models.base import Base
from services.firebase_service import get_current_active_user, get_current_user
import pytest
import os
from setup.config import get_settings
from fastapi.applications import FastAPI
from httpx import AsyncClient
from setup.start_app import start_app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from services.database_service import create_db_url, db
from typing import AsyncGenerator
from schema.user_schema import User, UserInDB
from typing import Generator
from _pytest.fixtures import SubRequest
from asyncio import get_event_loop_policy
from datetime import datetime

os.environ["ENV"] = "TEST"
engine = create_async_engine(create_db_url(), echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="session")
def test_user() -> User:
    return User(
        uid="123",
        username="DefiKid123",
        email="defikid123@maxfarms.zil",
        firstname="James",
        lastname="Holden",
        deleted=False,
    )


@pytest.fixture(scope="session")
def test_user_in_db() -> User:
    return UserInDB(
        id=1,
        uid="123",
        username="DefiKid123",
        email="defikid123@maxfarms.zil",
        firstname="James",
        lastname="Holden",
        deleted=False,
    )


@pytest.fixture(scope="session")
def test_program() -> Program:
    return Program(
        title="Test Title",
        slug="test-title",
        courses=[
            Course(
                title="Test Course 1",
                slug="test-course-1",
                lessons=[
                    Lesson(
                        title="Test Lesson 1",
                        slug="test-lesson-1",
                        sections=[
                            Section(
                                title="Test Section 1",
                                slug="test-section-1",
                                body="Body memes",
                            )
                        ],
                    )
                ],
            ),
            Course(
                title="Test Course 2",
                slug="test-course-2",
                lessons=[
                    Lesson(
                        title="Test Lesson 1-2",
                        slug="test-lesson-1-2",
                        sections=[
                            Section(
                                title="Test Section 1-2",
                                slug="test-section-1-2",
                                body="Body memes 2",
                            )
                        ],
                    )
                ],
            ),
        ],
    )


@pytest.fixture(scope="session")
def test_program_in_db() -> ProgramInDB:
    return ProgramInDB(
        id=1,
        title="Test Title",
        slug="test-title",
        created_on=datetime.now(),
        updated_on=datetime.now(),
        courses=[
            CourseInDB(
                id=1,
                title="Test Course 1",
                slug="test-course-1",
                likes=0,
                dislikes=0,
                created_on=datetime.now(),
                updated_on=datetime.now(),
                lessons=[
                    LessonInDB(
                        id=1,
                        title="Test Lesson 1",
                        slug="test-lesson-1",
                        likes=0,
                        dislikes=0,
                        created_on=datetime.now(),
                        updated_on=datetime.now(),
                        sections=[
                            SectionInDB(
                                id=1,
                                title="Test Section 1",
                                slug="test-section-1",
                                body="Body memes",
                                likes=0,
                                dislikes=0,
                                created_on=datetime.now(),
                                updated_on=datetime.now(),
                            )
                        ],
                    )
                ],
            ),
            CourseInDB(
                id=2,
                title="Test Course 2",
                slug="test-course-2",
                likes=0,
                dislikes=0,
                created_on=datetime.now(),
                updated_on=datetime.now(),
                lessons=[
                    LessonInDB(
                        id=2,
                        title="Test Lesson 1-2",
                        slug="test-lesson-1-2",
                        likes=0,
                        dislikes=0,
                        created_on=datetime.now(),
                        updated_on=datetime.now(),
                        sections=[
                            SectionInDB(
                                id=2,
                                title="Test Section 1-2",
                                slug="test-section-1-2",
                                body="Body memes 2",
                                likes=0,
                                dislikes=0,
                                created_on=datetime.now(),
                                updated_on=datetime.now(),
                            )
                        ],
                    )
                ],
            ),
        ],
    )


@pytest.fixture(scope="session")
def event_loop(request: SubRequest) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def fastapi_app_mock(test_user_in_db: UserInDB) -> FastAPI:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # type: ignore
        await conn.run_sync(Base.metadata.create_all)  # type: ignore
    app = start_app()
    app.dependency_overrides[db.get_db] = get_test_db
    app.dependency_overrides[get_current_active_user] = lambda: test_user_in_db
    app.dependency_overrides[get_current_user] = lambda: test_user_in_db
    return app


@pytest.fixture(scope="session")
def test_client(fastapi_app_mock: FastAPI) -> AsyncClient:
    return AsyncClient(
        app=fastapi_app_mock, base_url=f"http://localhost{get_settings().api_v1_str}"
    )
