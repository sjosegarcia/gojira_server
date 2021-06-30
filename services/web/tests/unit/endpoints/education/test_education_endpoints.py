import pytest
from httpx import AsyncClient
from schema.education_schema import Program, ProgramInDB
from fastapi import status


@pytest.mark.asyncio
async def test_create_program_endpoint(
    test_client: AsyncClient, test_program: Program
) -> None:
    response = await test_client.put(
        "/education/program/create", json=test_program.dict()
    )
    assert response.status_code == status.HTTP_200_OK
    program_in_db = ProgramInDB(**response.json())
    assert program_in_db.slug == test_program.slug


@pytest.mark.asyncio
async def test_get_program_by_id_endpoint(
    test_client: AsyncClient, test_program_in_db: ProgramInDB
) -> None:
    response = await test_client.get(f"/education/program/{test_program_in_db.id}")
    assert response.status_code == status.HTTP_200_OK
    program_in_db = ProgramInDB(**response.json())
    assert program_in_db.id == test_program_in_db.id


@pytest.mark.asyncio
async def test_get_all_programs_endpoint(test_client: AsyncClient) -> None:
    response = await test_client.get("/education/program/all")
    assert response.status_code == status.HTTP_200_OK
