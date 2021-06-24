from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from schema.user_schema import User, UserInDB


@pytest.mark.asyncio
async def test_create_new_user(client: TestClient) -> None:
    response = client.put(
        "/user/new",
        data=User(
            uid="",
            username="DefiKid123",
            email="defikid123@maxfarms.zil",
            firstname="James",
            lastname="Holden",
            dob=datetime(year=1980, month=1, day=6),
        ).json(),
    )
    assert response.status_code == 200
    user_in_db = UserInDB(**response.json())
    assert user_in_db.id
