from fastapi.param_functions import Header, Security
from repositories.user_repository import get_user_by_uid
from firebase_admin import credentials, exceptions, auth, initialize_app
from sqlalchemy.ext.asyncio.session import AsyncSession
from setup.config import get_settings
from firebase_admin.auth import UserRecord
from datetime import timedelta, datetime
from time import time
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from schema.user_schema import UserInDB
from repositories.database_repository import db
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{get_settings().api_v1_str}/authentication/token",
    scopes={"me": "Read information about the current user."},
)


def init_sdk_with_service_account() -> None:
    cred = credentials.Certificate(get_settings().gcp_service_account_key_path)
    initialize_app(cred)


def get_user(uid: str) -> UserRecord:
    return auth.get_user(uid)


def delete_user(uid: str) -> None:
    auth.delete_user(uid)


def verify_id_token(id_token: str) -> str:
    try:
        # Verify the ID token while checking if the token is revoked by
        # passing check_revoked=True.
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        # Token is valid and not revoked.
        uid = decoded_token["uid"]
    except auth.RevokedIdTokenError:
        # Token revoked, inform the user to reauthenticate or signOut().
        pass
    except auth.InvalidIdTokenError:
        pass
    return str(uid)


def check_auth_time(id_token: str) -> ORJSONResponse:
    # To ensure that cookies are set only on recently signed in users, check auth_time in
    # ID token before creating a cookie.
    try:
        decoded_claims = auth.verify_id_token(id_token)
        # Only process if the user signed in within the last 5 minutes.
        if time() - decoded_claims["auth_time"] < 5 * 60:
            expires_in = timedelta(days=5)
            expires = datetime.now() + expires_in
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            response = ORJSONResponse({"status": "success"})
            response.set_cookie(
                "session",
                session_cookie,
                expires=int(expires.strftime("%Y%m%d%H%M%S")),
                httponly=True,
                secure=True,
            )

        # User did not sign in recently. To guard against ID token theft, require
        # re-authentication.
        # raise HTTPException(status_code=401, detail="Need to sign in again")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except exceptions.FirebaseError:
        raise HTTPException(status_code=401, detail="Failed to create a session cookie")
    return response


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(db.get_db),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        id_token = authorization.split(" ")[1]
        if not id_token:
            raise HTTPException(status_code=401, detail=f"Could not grab id token")
        uid = verify_id_token(id_token)
    except (auth.RevokedIdTokenError, auth.InvalidIdTokenError):
        raise credentials_exception
    user_in_db = await get_user_by_uid(db, uid)
    if user_in_db is None:
        raise credentials_exception
    user = UserInDB.from_orm(user_in_db)
    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    if current_user.deleted:
        raise HTTPException(status_code=400, detail="This user account is inactive")
    return current_user
