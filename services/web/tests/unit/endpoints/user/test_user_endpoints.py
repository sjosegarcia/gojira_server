import pytest
from pytest_mock import MockerFixture
from httpx import AsyncClient
from schema.user_schema import User, UserInDB
from fastapi import status


@pytest.mark.asyncio
async def test_create_new_user(
    test_client: AsyncClient, test_user: User, mocker: MockerFixture
) -> None:
    mocker.patch("firebase_admin.auth.set_custom_user_claims")
    response = await test_client.put(
        "/user/new",
        json=test_user.dict(),
    )
    assert response.status_code == status.HTTP_200_OK
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_create_new_user_failed(
    test_client: AsyncClient, test_user: User, mocker: MockerFixture
) -> None:
    mocker.patch("firebase_admin.auth.set_custom_user_claims")
    response = await test_client.put(
        "/user/new",
        json=test_user.dict(),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_user_id(
    test_client: AsyncClient, test_user: User, test_user_in_db: UserInDB
) -> None:
    response = await test_client.get(f"/user/id/{test_user_in_db.id}")
    assert response.status_code == status.HTTP_200_OK
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_get_user_id_failed(test_client: AsyncClient, test_user: User) -> None:
    response = await test_client.get(f"/user/id/2")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_authenticated_user(
    test_client: AsyncClient, test_user: User
) -> None:
    response = await test_client.get(f"/user/me")
    assert response.status_code == status.HTTP_200_OK
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid


@pytest.mark.asyncio
async def test_delete_current_user(test_client: AsyncClient, test_user: User) -> None:
    response = await test_client.delete("/user/me/delete")
    assert response.status_code == status.HTTP_200_OK
    user_in_db = UserInDB(**response.json())
    assert user_in_db.uid == test_user.uid
