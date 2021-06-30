import pytest
from pytest_mock import MockerFixture
from httpx import AsyncClient
from schema.user_schema import User, UserInDB


@pytest.mark.asyncio
async def test_create_new_user(
    test_client: AsyncClient, test_user: User, mocker: MockerFixture
) -> None:
    mocker.patch("firebase_admin.auth.set_custom_user_claims")
    async with test_client as client:
        response = await client.put(
            "/user/new",
            json=test_user.dict(),
        )
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_get_user_id(test_client: AsyncClient, test_user: User) -> None:
    async with test_client as client:
        response = await client.get(f"/user/id/1")
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_get_authenticated_user(
    test_client: AsyncClient, test_user: User
) -> None:
    async with test_client as client:
        response = await client.get(f"/user/me")
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    # assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_delete_current_user(test_client: AsyncClient, test_user: User) -> None:
    async with test_client as client:
        response = await client.delete("/user/me/delete")
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    assert user_in_db.email == test_user.email


"""
@pytest.mark.asyncio
async def test_create_new_user_failed(
    test_client: AsyncClient, test_user: User, mocker: MockerFixture
) -> None:
    mocker.patch("firebase_admin.auth.set_custom_user_claims")
    failed_user = deepcopy(test_user.dict())
    async with test_client as client:
        response = await client.put(
            "/user/new",
            json=failed_user,
        )
    assert response.status_code == 400"""


"""
@pytest.mark.asyncio
async def test_delete_current_user_failed(
    test_client: AsyncClient, test_user: User
) -> None:  # josh@aboutfresh.org jallen@mass-ventures.com
    async with test_client as client:
        response = await client.delete("/user/me/delete")
    assert response.status_code == 405
"""
