from repositories.firebase_repository import get_current_user
from fastapi import Depends, Security
from fastapi.routing import APIRouter
from schema.education_schema import (
    Program,
    Section,
    Course,
    Lesson,
    ProgramInDB,
    SectionInDB,
    CourseInDB,
    LessonInDB,
)
from schema.user_schema import UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.database_repository import db
from starlette.requests import Request
from repositories.education_repository import (
    get_lesson_by_id,
    get_program_by_id,
    get_all_programs,
    create_program,
)
from fastapi.exceptions import HTTPException
from typing import List

education_router = APIRouter()


@education_router.get("/program/{program_id}", response_model=ProgramInDB)
async def get_program_by_id_endpoint(
    program_id: int, db: AsyncSession = Depends(db.get_db)
) -> ProgramInDB:
    program_found = await get_program_by_id(db, program_id)
    if program_found:
        raise HTTPException(status_code=400, detail="Program not found.")
    return ProgramInDB.from_orm(program_found)


@education_router.get("/program/all", response_model=List[ProgramInDB])
async def get_all_programs_endpoint(
    db: AsyncSession = Depends(db.get_db),
) -> List[ProgramInDB]:
    programs = await get_all_programs(db)
    return [ProgramInDB.from_orm(program) for program in programs]


@education_router.put("/program/create", response_model=ProgramInDB)
async def create_program_endpoint(
    request: Request,
    db: AsyncSession = Depends(db.get_db),
    current_user: UserInDB = Security(get_current_user, scopes=["editor", "admin"]),
) -> ProgramInDB:
    data = await request.json()
    program = Program(**data)
    new_program = create_program(db, program)
    return ProgramInDB.from_orm(new_program)


@education_router.get("/lesson/{lesson_id}", response_model=LessonInDB)
async def get_lesson_by_id_endpoint(
    lesson_id: int, db: AsyncSession = Depends(db.get_db)
) -> LessonInDB:
    lesson_found = await get_lesson_by_id(db, lesson_id)
    if lesson_found:
        raise HTTPException(status_code=400, detail="Lesson not found.")
    return LessonInDB.from_orm(lesson_found)


@education_router.get("/course/{course_id}", response_model=CourseInDB)
async def get_course_by_id_endpoint(
    course_id: int, db: AsyncSession = Depends(db.get_db)
) -> CourseInDB:
    course_found = await get_lesson_by_id(db, course_id)
    if course_found:
        raise HTTPException(status_code=400, detail="Course not found.")
    return CourseInDB.from_orm(course_found)


@education_router.get("/section/{section_id}", response_model=SectionInDB)
async def get_section_by_id_endpoint(
    section_id: int, db: AsyncSession = Depends(db.get_db)
) -> SectionInDB:
    section_found = await get_lesson_by_id(db, section_id)
    if section_found:
        raise HTTPException(status_code=400, detail="Section not found.")
    return SectionInDB.from_orm(section_found)