# mypy: ignore-errors
from fastapi.param_functions import Header, Security
from crud.user_crud import get_user_by_uid
from firebase_admin import App, initialize_app, delete_app
from firebase_admin.credentials import Certificate
from firebase_admin.exceptions import FirebaseError

from firebase_admin.auth import (
    get_user,
    delete_user,
    verify_id_token,
    set_custom_user_claims,
    UserNotFoundError,
    RevokedIdTokenError,
    InvalidIdTokenError,
    UserRecord,
    create_session_cookie,
)

from sqlalchemy.ext.asyncio.session import AsyncSession
from setup.config import get_settings
from datetime import timedelta, datetime
from time import time
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from schema.user_schema import UserInDB
from services.database_service import db
from fastapi.security import SecurityScopes


def get_credentials() -> Certificate:
    return Certificate(get_settings().gcp_service_account_key_path)


def init_sdk_with_service_account() -> None:
    initialize_app(get_credentials())


def remove_sdk_with_service_account(app: App) -> None:
    delete_app(app)


def get_firebase_user(uid: str) -> UserRecord:
    try:
        return get_user(uid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a proper UID",
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user, User ID could not be found.",
        )


def delete_user(uid: str) -> None:
    try:
        delete_user(uid)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not delete user, User ID could not be found.",
        )


def _verify_id_token(id_token: str) -> dict:
    try:
        decoded_token = verify_id_token(id_token, check_revoked=True)
    except RevokedIdTokenError:
        # Token revoked, inform the user to reauthenticate or signOut().
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked, please sign out and try again.",
        )
    except InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token.",
        )
    return dict(decoded_token)


def apply_custom_claim(uid: str, claims: dict) -> None:
    try:
        set_custom_user_claims(uid, claims)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not apply claim, User ID could not be found.",
        )


def add_scope(uid: str, new_scope: str) -> bool:
    user = get_firebase_user(uid)
    claims = dict(user.custom_claims)
    scopes = claims.get("scopes", [])
    if scopes:
        if new_scope in scopes:
            return True
        scopes.append(new_scope)
        apply_custom_claim(uid, {"scopes": scopes})
        return True
    return False


def check_auth_time(id_token: str) -> ORJSONResponse:
    # To ensure that cookies are set only on recently signed in users, check auth_time in
    # ID token before creating a cookie.
    try:
        decoded_claims = _verify_id_token(id_token)
        # Only process if the user signed in within the last 5 minutes.
        if time() - decoded_claims["auth_time"] < 5 * 60:
            expires_in = timedelta(days=5)
            expires = datetime.now() + expires_in
            session_cookie = create_session_cookie(id_token, expires_in=expires_in)
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
    except InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ID token"
        )
    except FirebaseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to create a session cookie",
        )
    return response


async def get_current_user(
    security_scopes: SecurityScopes,
    authorization: str = Header(None),
    db: AsyncSession = Depends(db.get_db),
) -> UserInDB:

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        id_token = authorization.split(" ")[1]
        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not grab id token",
            )
        decoded_token = _verify_id_token(id_token)
    except (RevokedIdTokenError, InvalidIdTokenError):
        raise credentials_exception
    user_in_db = await get_user_by_uid(db, decoded_token["uid"])
    if user_in_db is None:
        raise credentials_exception
    user = UserInDB.from_orm(user_in_db)
    scopes = list(decoded_token["scopes"])
    if "admin" not in scopes:
        for scope in security_scopes.scopes:
            if scope not in scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    return user


async def get_current_active_user(
    current_user: UserInDB = Security(get_current_user, scopes=["me"]),
) -> UserInDB:
    if current_user.deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user account is inactive",
        )
    return current_user
