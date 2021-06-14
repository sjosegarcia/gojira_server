from fastapi import Depends
from fastapi.routing import APIRouter
from schema.education_schema import Program
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.database_repository import db
from starlette.requests import Request
from repositories.education_repository import (
    get_program_by_id,
    get_all_programs,
    create_program,
)
from fastapi.exceptions import HTTPException
from typing import List

program_router = APIRouter()


@program_router.get("/programs/{program_id}", response_model=Program)
async def get_program_by_id_endpoint(
    program_id: int, db: AsyncSession = Depends(db.get_db)
) -> Program:
    program_found = await get_program_by_id(db, program_id)
    if program_found:
        raise HTTPException(status_code=400, detail="Program not found.")
    return Program.from_orm(program_found)


@program_router.get("/programs/all", response_model=List[Program])
async def get_all_programs_endpoint(
    db: AsyncSession = Depends(db.get_db),
) -> List[Program]:
    programs = await get_all_programs(db)
    return [Program.from_orm(program) for program in programs]


@program_router.put("/program/create", response_model=Program)
async def create_program_endpoint(
    request: Request, db: AsyncSession = Depends(db.get_db)
) -> Program:
    data = await request.json()
    program = Program(**data)
    new_program = create_program(db, program)
    return Program.from_orm(new_program)
