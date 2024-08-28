import os
from collections.abc import Generator
from datetime import timedelta
from sqlalchemy import exc, select
from sqlalchemy.orm import Session, sessionmaker
from itsdangerous import BadSignature, URLSafeTimedSerializer, SignatureExpired
from starlette import status

from .database import engine

from fastapi import (
    HTTPException,
    Request,
    Response,
)
from fastapi.responses import RedirectResponse

from .models.user import User


def get_db_session() -> Generator[Session, None, None]:
    factory = sessionmaker(engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError as error:
            session.rollback()
            raise error
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.close()


SECRET_KEY = "my-secret-key"
SESSION_MAX_AGE = int(timedelta(days=30).total_seconds())
timed_serializer = URLSafeTimedSerializer(SECRET_KEY)


def get_current_user(request: Request, session: Session) -> User | None:
    session_cookie = request.cookies.get("sess")
    if not session_cookie:
        return None
    try:
        user = timed_serializer.loads(session_cookie, max_age=SESSION_MAX_AGE)
        db_user = User.get_by_email(session=session, email=user["email"])
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    except BadSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    return db_user


def login_user(user, redirect_url: str) -> Response:
    # secure = os.getenv("APP_ENV") == "PROD"

    session_data = timed_serializer.dumps({"user_id": user.id, "email": user.email})
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key="sess",
        value=session_data,
        httponly=True,
        # secure=secure,  # Set to True in a HTTPS environment
        max_age=SESSION_MAX_AGE,
        samesite="lax",
    )
    return response


def get_user_from_session(cookie_value: str, db: Session):
    try:
        # Deserialize the session data
        session_data = timed_serializer.loads(cookie_value)
        user_id = session_data.get("user_id")

        # Query the user from the database using SQLAlchemy 2.0 syntax
        stmt = select(User).where(User.id == user_id)
        user = db.scalars(stmt).one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid session or user does not exist")

        return user
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="Invalid or expired session")