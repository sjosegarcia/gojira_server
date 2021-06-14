from sqlalchemy.ext.asyncio.session import AsyncSession
from models.education_model import Program
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
