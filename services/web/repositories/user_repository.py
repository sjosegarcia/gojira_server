from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.user_schema import User as UserSchema
from models.user_model import User
from sqlalchemy import select


async def create_user(db: AsyncSession, user: UserSchema) -> User:
    new_user = User(
        email=user.email,
        username=user.username,
        first_name=user.firstname,
        last_name=user.lastname,
        email_verified=False,
        dob=user.dob,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()