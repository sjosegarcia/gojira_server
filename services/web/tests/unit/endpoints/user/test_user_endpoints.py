import pytest
from httpx import AsyncClient
from schema.user_schema import User, UserInDB


@pytest.mark.asyncio
async def test_create_new_user(test_client: AsyncClient) -> None:
    async with test_client as client:
        response = await client.put(
            "/user/new",
            json=User(
                uid="123",
                username="DefiKid123",
                email="defikid123@maxfarms.zil",
                firstname="James",
                lastname="Holden",
            ).dict(),
        )
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    assert user_in_db.id
