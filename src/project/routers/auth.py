import os
import shutil
from pathlib import Path
from typing import Annotated
from urllib.parse import urlsplit

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from ..dependencies import (
    get_current_user,
    get_db_session,
    login_user,
    oauth,
    templates,
)
from ..models.user import User
from ..utils.additional_func_auth import hash_password, pwd_context
from ..utils.enums import OauthProvider
from ..utils.errors.error_messages import (
    EMAIL_ALREADY_REGISTERED,
    GOOGLE_USER,
    INCORRECT_PASSWORD,
    NOT_ENOUGH_PERMISSION,
    OAUTH_NO_EMAIL,
    OAUTH_NO_USER_INFO,
    PASSWORD_REQUIRED,
    PASSWORDS_DO_NOT_MATCH,
    USER_NOT_FOUND,
)
from ..utils.errors.errors import UserDataError

router = APIRouter()

UPLOAD_DIR = Path("src/project/static/images/profile_pictures")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Gets register template
@router.get("/register", tags=["auth"], response_class=HTMLResponse)
async def get_register_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("register.html", {"request": request})


# Post view for user registration
@router.post("/register", tags=["auth"], response_class=HTMLResponse)
async def post_register_user(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    db: Session = Depends(get_db_session),
) -> RedirectResponse:
    if not password:
        return HTMLResponse(content=PASSWORD_REQUIRED, status_code=400)

    if password != confirm_password:
        return HTMLResponse(content=PASSWORDS_DO_NOT_MATCH, status_code=400)

    hashed_password = hash_password(password)
    try:
        new_user = User(
            email=email,
            password=hashed_password,
            oauth_provider=OauthProvider.ORDINARY_USER,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse(url="/login", status_code=303)
    except IntegrityError:
        db.rollback()
        return HTMLResponse(content=EMAIL_ALREADY_REGISTERED, status_code=400)


# Gets login template
@router.get("/login", tags=["auth"], response_class=HTMLResponse)
async def get_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("/login.html", {"request": request})


# Post view for user login
@router.post("/login", tags=["auth"], response_class=HTMLResponse)
async def post_login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db_session),
) -> Response:
    user = User.get_by_email(db, email)
    if not user:
        return HTMLResponse(content=USER_NOT_FOUND, status_code=400)
    if user.oauth_provider == OauthProvider.GOOGLE:
        return HTMLResponse(content=GOOGLE_USER, status_code=400)
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail=INCORRECT_PASSWORD)
    user_data = {"id": user.id, "email": user.email}
    response = login_user(user=user_data, redirect_url="/index")
    return response


@router.get("/logout")
async def logout(request: Request, response: Response) -> Response:
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="sess")
    return response


# Google Authentication
def oauth_user(email: str, oauth_provider: OauthProvider, session: Session):
    try:
        user = User.get_by_email(session=session, email=email)
        if not user:
            user = User(email=email, oauth_provider=oauth_provider)
            session.add(user)
            session.commit()
            session.refresh(user)
        return {"email": user.email}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        session.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))


@router.get("/google_login", tags=["auth"])
async def google_login(request: Request):
    scheme = "https" if os.getenv("APP_ENV") == "PROD" else "http"
    https_request = Request(
        scope={
            **request.scope,
            "scheme": scheme,
            "url": urlsplit(str(request.url))._replace(scheme="https").geturl(),
        },
        receive=request._receive,
    )
    return await oauth.google.authorize_redirect(https_request, redirect_uri=https_request.url_for("google_callback"))


@router.get("/google-oauth", tags=["auth"])
async def google_callback(
    request: Request,
    session: Session = Depends(get_db_session),
):
    try:
        token = await oauth.google.authorize_access_token(request)  # type: ignore
    except Exception as e:
        raise UserDataError(status_code=400, detail=str(e))
    google_user_info = token.get("userinfo")
    if not google_user_info:
        raise UserDataError(status_code=303, detail=OAUTH_NO_USER_INFO)
    email = google_user_info.get("email")
    if not email:
        raise UserDataError(status_code=303, detail=OAUTH_NO_EMAIL)
    try:
        user = oauth_user(email=email, session=session, oauth_provider=OauthProvider.GOOGLE)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = login_user(user=user, redirect_url="/index")
    return response


# Returns index page
@router.get("/index", tags=["auth"])
async def get_index(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request, session)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_ENOUGH_PERMISSION)
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})


# Returns the update page and updates the user detail
@router.api_route("/settings", methods=["GET", "POST"], tags=["auth"], response_model=None)
async def settings(
    request: Request,
    first_name: Annotated[str, Form()] = None,
    last_name: Annotated[str, Form()] = None,
    username: Annotated[str, Form()] = None,
    email: Annotated[str, Form()] = None,
    about: Annotated[str, Form()] = None,
    picture_url: Annotated[UploadFile, File()] = None,
    session: Session = Depends(get_db_session),
):
    current_user = get_current_user(request, session)
    if request.method == "GET":
        if not get_current_user(request, session):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_ENOUGH_PERMISSION)
        return templates.TemplateResponse("settings.html", {"request": request, "user": current_user})
    elif request.method == "POST":
        try:
            old_email = current_user.email
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.username = username
            current_user.email = email
            current_user.about = about
            if picture_url and picture_url.filename != "":
                file_path = UPLOAD_DIR / picture_url.filename
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(picture_url.file, buffer)
                current_user.picture_url = f"/static/images/profile_pictures/{picture_url.filename}"
            session.commit()

            if old_email != email:
                return RedirectResponse(url="/login", status_code=303)
        except Exception as e:
            session.rollback()  # Rollback the transaction on error
            return RedirectResponse(
                url="/settings", status_code=303, headers={"X-Error": f"An error occurred while updating {e}"}
            )
        return RedirectResponse(url="/settings", status_code=303)


# Deletes the account
@router.delete("/delete_account/{user_id}", tags=["auth"])
async def delete_account(user_id: int, session: Session = Depends(get_db_session)):
    User.delete(session, user_id)
    return RedirectResponse(url="/login", status_code=303)
