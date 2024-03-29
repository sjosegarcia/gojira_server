from services.firebase_service import get_current_user
from fastapi import Depends, Security, status
from fastapi.routing import APIRouter
from schema.education_schema import (
    Program,
    ProgramInDB,
    SectionInDB,
    CourseInDB,
    LessonInDB,
)
from schema.user_schema import UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from services.database_service import db
from starlette.requests import Request
from crud.education_crud import (
    get_course_by_id,
    get_lesson_by_id,
    get_program_by_id,
    get_all_programs,
    create_program,
    get_section_by_full_slug,
    get_lesson_by_slug,
    get_course_by_slug,
    get_program_by_slug,
    get_section_by_id,
)
from fastapi.exceptions import HTTPException
from typing import List

education_router = APIRouter()


@education_router.get("/program/{program_id}", response_model=ProgramInDB)
async def get_program_by_id_endpoint(
    program_id: int, db: AsyncSession = Depends(db.get_db)
) -> ProgramInDB:
    program_found = await get_program_by_id(db, program_id)
    if not program_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Program not found."
        )
    return ProgramInDB.from_orm(program_found)


@education_router.get("/program/all/", response_model=List[ProgramInDB])
async def get_all_programs_endpoint(
    db: AsyncSession = Depends(db.get_db),
) -> List[ProgramInDB]:
    programs = await get_all_programs(db)
    return [ProgramInDB.from_orm(program) for program in programs]


@education_router.post("/program/create", response_model=ProgramInDB)
async def create_program_endpoint(
    request: Request,
    db: AsyncSession = Depends(db.get_db),
    current_user: UserInDB = Security(get_current_user, scopes=["editor"]),
) -> ProgramInDB:
    data = await request.json()
    new_program_schema = Program(**data)
    new_program = await create_program(db, new_program_schema)
    return ProgramInDB.from_orm(new_program)


@education_router.get(
    "/{program_slug}/{course_slug}/{lesson_slug}/{section_slug}",
    response_model=SectionInDB,
)
async def get_section_by_url_slug(
    program_slug: str,
    course_slug: str,
    lesson_slug: str,
    section_slug: str,
    db: AsyncSession = Depends(db.get_db),
) -> SectionInDB:
    section_found = await get_section_by_full_slug(
        db, program_slug, course_slug, lesson_slug, section_slug
    )
    if not section_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section not found."
        )
    return SectionInDB.from_orm(section_found)


@education_router.get(
    "/{program_slug}/{course_slug}/{lesson_slug}",
    response_model=LessonInDB,
)
async def get_lesson_by_url_slug(
    program_slug: str,
    course_slug: str,
    lesson_slug: str,
    db: AsyncSession = Depends(db.get_db),
) -> LessonInDB:
    lesson_found = await get_lesson_by_slug(db, program_slug, course_slug, lesson_slug)
    if not lesson_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found."
        )
    return LessonInDB.from_orm(lesson_found)


@education_router.get(
    "/{program_slug}/{course_slug}",
    response_model=CourseInDB,
)
async def get_course_by_url_slug(
    program_slug: str,
    course_slug: str,
    db: AsyncSession = Depends(db.get_db),
) -> CourseInDB:
    course_found = await get_course_by_slug(db, program_slug, course_slug)
    if not course_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found."
        )
    return CourseInDB.from_orm(course_found)


@education_router.get(
    "/{program_slug}",
    response_model=ProgramInDB,
)
async def get_program_by_url_slug(
    program_slug: str,
    db: AsyncSession = Depends(db.get_db),
) -> ProgramInDB:
    program_found = await get_program_by_slug(db, program_slug)
    if not program_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Program not found."
        )
    return ProgramInDB.from_orm(program_found)
