from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.user_schema import User as UserSchema, UserInDB
from models.user_model import User
from sqlalchemy import select


async def create_user(db: AsyncSession, user: UserSchema) -> User:
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(
        select(User).where(User.email == email and User.deleted == False)
    )
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, id: int) -> User:
    result = await db.execute(
        select(User).where(User.id == id and User.deleted == False)
    )
    return result.scalars().first()


async def get_user_by_uid(db: AsyncSession, uid: str) -> User:
    result = await db.execute(
        select(User).where(User.uid == uid and User.deleted == False)
    )
    return result.scalars().first()


async def delete_user(db: AsyncSession, id: int) -> User:
    user_found = await get_user_by_id(db, id)
    if user_found:
        user_found.deleted = True
        await db.commit()
    return user_found


async def update_user(db: AsyncSession, old_user: UserInDB) -> User:
    pass
