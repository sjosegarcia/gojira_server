from fastapi.routing import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.database_repository import db
from schema.user_schema import User, UserInDB
from fastapi.exceptions import HTTPException
from repositories.user_repository import create_user, get_user_by_email, get_user_by_id
from starlette.requests import Request

users_router = APIRouter()


@users_router.put("/new-user", response_model=UserInDB)
async def create_new_user(
    user: User, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:

    user_found = await get_user_by_email(db, user.email)
    if user_found:
        raise HTTPException(status_code=400, detail="User already exist.")

    new_user = create_user(db, user)
    return UserInDB.from_orm(new_user)


@users_router.get("/get-user-id", response_model=UserInDB)
async def get_user_id(
    request: Request, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:
    data = await request.json()
    user_found = await get_user_by_id(db, data["id"])
    if not user_found:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return UserInDB.from_orm(user_found)


@users_router.get("/get-user-email", response_model=UserInDB)
async def get_user_email(
    request: Request, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:
    data = await request.json()
    user_found = await get_user_by_email(db, data["email"])
    if not user_found:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return UserInDB.from_orm(user_found)


@users_router.post("/update-user", response_model=UserInDB)
async def update_user(
    request: Request, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:
    pass
