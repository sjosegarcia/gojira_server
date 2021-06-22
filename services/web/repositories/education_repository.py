from sqlalchemy.ext.asyncio.session import AsyncSession
from models.education_model import Course, Lesson, Program, Section
from schema.education_schema import Program as ProgramSchema
from sqlalchemy import select


async def get_program_by_id(db: AsyncSession, id: int) -> Program:
    result = await db.execute(select(Program).where(Program.id == id))
    return result.scalars().first()


async def get_all_programs(
    db: AsyncSession,
) -> list[Program]:
    result = await db.execute(select(Program))
    return result.scalars().all()


async def create_program(db: AsyncSession, program: ProgramSchema) -> Program:
    new_program = Program(**program.dict())
    db.add(new_program)
    await db.commit()
    return new_program


async def get_section_by_id(db: AsyncSession, id: int) -> Section:
    result = await db.execute(select(Section).where(Section.id == id))
    return result.scalars().first()


async def get_course_by_id(db: AsyncSession, id: int) -> Course:
    result = await db.execute(select(Course).where(Course.id == id))
    return result.scalars().first()


async def get_lesson_by_id(db: AsyncSession, id: int) -> Lesson:
    result = await db.execute(select(Lesson).where(Lesson.id == id))
    return result.scalars().first()


async def get_section_by_full_slug(
    db: AsyncSession,
    program_slug: str,
    course_slug: str,
    lesson_slug: str,
    section_slug: str,
) -> Section:
    result = await db.execute(
        select(Section)
        .where(Section.slug == section_slug)
        .join(Lesson)
        .filter(Lesson.slug == lesson_slug)
        .join(Course)
        .filter(Course.slug == course_slug)
        .join(Program)
        .filter(Program.slug == program_slug)
    )
    return result.scalars().first()


async def get_section_by_slug(
    db: AsyncSession,
    section_slug: str,
) -> Section:
    result = await db.execute(select(Section).where(Section.slug == section_slug))
    return result.scalars().first()


async def get_lesson_by_slug(
    db: AsyncSession,
    program_slug: str,
    course_slug: str,
    lesson_slug: str,
) -> Section:
    result = await db.execute(
        select(Lesson)
        .where(Lesson.slug == lesson_slug)
        .join(Course)
        .filter(Course.slug == course_slug)
        .join(Program)
        .filter(Program.slug == program_slug)
    )
    return result.scalars().first()


async def get_course_by_slug(
    db: AsyncSession,
    program_slug: str,
    course_slug: str,
) -> Section:
    result = await db.execute(
        select(Course)
        .where(Course.slug == course_slug)
        .join(Program)
        .filter(Program.slug == program_slug)
    )
    return result.scalars().first()


async def get_program_by_slug(
    db: AsyncSession,
    program_slug: str,
) -> Program:
    result = await db.execute(select(Program).where(Program.slug == program_slug))
    return result.scalars().first()
