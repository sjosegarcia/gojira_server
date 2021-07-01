import pytest
from httpx import AsyncClient
from schema.education_schema import (
    Program,
    ProgramInDB,
    SectionInDB,
    LessonInDB,
    CourseInDB,
)
from fastapi import status


@pytest.mark.asyncio
async def test_create_program_endpoint(
    test_client: AsyncClient, test_program: Program
) -> None:
    async with test_client as client:
        response = await client.post(
            "/education/program/create", json=test_program.dict()
        )
    assert response.status_code == status.HTTP_200_OK
    program_in_db = ProgramInDB(**response.json())
    assert program_in_db.slug == test_program.slug


@pytest.mark.asyncio
async def test_get_program_by_id_endpoint(
    test_client: AsyncClient, test_program_in_db: ProgramInDB
) -> None:
    async with test_client as client:
        response = await client.get(f"/education/program/{test_program_in_db.id}")
    assert response.status_code == status.HTTP_200_OK
    program_in_db = ProgramInDB(**response.json())
    assert program_in_db.id == test_program_in_db.id


@pytest.mark.asyncio
async def test_get_all_programs_endpoint(test_client: AsyncClient) -> None:
    async with test_client as client:
        response = await client.get("/education/program/all/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_section_by_url_slug(
    test_client: AsyncClient, test_program: Program
) -> None:
    async with test_client as client:
        response = await client.get(
            f"/education/{test_program.slug}/{test_program.courses[0].slug}/{test_program.courses[0].lessons[0].slug}/{test_program.courses[0].lessons[0].sections[0].slug}"
        )
    assert response.status_code == status.HTTP_200_OK
    section_in_db = SectionInDB(**response.json())
    assert test_program.courses[0].lessons[0].sections[0].slug == section_in_db.slug


@pytest.mark.asyncio
async def test_get_lesson_by_url_slug(
    test_client: AsyncClient, test_program: Program
) -> None:
    async with test_client as client:
        response = await client.get(
            f"/education/{test_program.slug}/{test_program.courses[0].slug}/{test_program.courses[0].lessons[0].slug}"
        )
    assert response.status_code == status.HTTP_200_OK
    lesson_in_db = LessonInDB(**response.json())
    assert test_program.courses[0].lessons[0].slug == lesson_in_db.slug


@pytest.mark.asyncio
async def test_get_course_by_url_slug(
    test_client: AsyncClient, test_program: Program
) -> None:
    async with test_client as client:
        response = await client.get(
            f"/education/{test_program.slug}/{test_program.courses[0].slug}"
        )
    assert response.status_code == status.HTTP_200_OK
    course_in_db = CourseInDB(**response.json())
    assert test_program.courses[0].slug == course_in_db.slug


@pytest.mark.asyncio
async def test_get_program_by_url_slug(
    test_client: AsyncClient, test_program: Program
) -> None:
    async with test_client as client:
        response = await client.get(f"/education/{test_program.slug}")
    assert response.status_code == status.HTTP_200_OK
    program_in_db = ProgramInDB(**response.json())
    assert test_program.slug == program_in_db.slug
