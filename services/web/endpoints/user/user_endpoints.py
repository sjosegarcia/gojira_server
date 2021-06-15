from repositories.firebase_repository import get_current_active_user, verify_id_token
from fastapi.routing import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.database_repository import db
from schema.user_schema import User, UserInDB
from fastapi.exceptions import HTTPException
from repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    delete_user,
    get_user_by_uid,
)
from starlette.requests import Request

users_router = APIRouter()


@users_router.put("/user/new", response_model=UserInDB)
async def create_new_user(
    user: User, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:

    user_found = await get_user_by_email(db, user.email)
    if user_found:
        raise HTTPException(status_code=400, detail="User already exist.")

    new_user = create_user(db, user)
    return UserInDB.from_orm(new_user)


@users_router.get("/user/id/{user_id}", response_model=UserInDB)
async def get_user_id(user_id: int, db: AsyncSession = Depends(db.get_db)) -> UserInDB:
    user_found = await get_user_by_id(db, user_id)
    if not user_found:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return UserInDB.from_orm(user_found)


@users_router.post("/user/me/update", response_model=UserInDB)
async def update_user(
    request: Request, current_user: UserInDB = Depends(get_current_active_user)
) -> UserInDB:
    data = await request.json()
    print(current_user.dict())
    new_user = current_user.copy(update=data)
    print(new_user.dict())
    return new_user


@users_router.delete("/user/delete/{user_id}", response_model=UserInDB)
async def delete_user_by_id(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:
    user_deleted = await delete_user(db, user_id)
    if not user_deleted:
        raise HTTPException(status_code=405, detail="User does not exist.")
    return UserInDB.from_orm(user_deleted)


@users_router.get("/user/me", response_model=UserInDB)
async def get_authenticated_user(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    return current_user
