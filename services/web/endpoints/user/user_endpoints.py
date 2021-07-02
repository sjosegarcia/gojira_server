from services.firebase_service import get_current_active_user, apply_custom_claim
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.database_service import db
from schema.user_schema import User, UserInDB
from fastapi.exceptions import HTTPException
from crud.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    delete_user,
)
from starlette.requests import Request

users_router = APIRouter()


@users_router.put("/new", response_model=UserInDB)
async def create_new_user(
    request: Request, db: AsyncSession = Depends(db.get_db)
) -> UserInDB:
    data = await request.json()
    user_found = await get_user_by_email(db, data["email"])
    if user_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist."
        )
    new_user_schema = User(
        uid=data.get("uid", None),
        username=data.get("username", None),
        email=data.get("email", None),
        firstname=data.get("firstname", None),
        lastname=data.get("lastname", None),
        dob=data.get("dob", None),
        last_login_date=data.get("last_login_date", None),
        email_verified=data.get("email_verified", False),
        photo_url=data.get("photo_url", None),
    )
    new_user = await create_user(db, new_user_schema)
    user_in_db = UserInDB.from_orm(new_user)
    apply_custom_claim(user_in_db.uid, {"scopes": ["me"]})
    return user_in_db


@users_router.get("/id/{user_id}", response_model=UserInDB)
async def get_user_id(user_id: int, db: AsyncSession = Depends(db.get_db)) -> UserInDB:
    user_found = await get_user_by_id(db, user_id)
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found."
        )
    return UserInDB.from_orm(user_found)


@users_router.post("/me/update", response_model=UserInDB)
async def update_user(
    request: Request, current_user: UserInDB = Depends(get_current_active_user)
) -> UserInDB:
    data = await request.json()
    print(current_user.dict())
    new_user = current_user.copy(update=data)
    print(new_user.dict())
    return new_user


@users_router.delete("/me/delete", response_model=UserInDB)
async def delete_current_user(
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(db.get_db),
) -> UserInDB:
    user_deleted = await delete_user(db, current_user.id)
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User could not be deleted.",
        )
    return UserInDB.from_orm(user_deleted)


@users_router.get("/me", response_model=UserInDB)
async def get_authenticated_user(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    return current_user
