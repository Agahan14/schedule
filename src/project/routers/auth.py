import os
from typing import Annotated
from urllib.parse import urlsplit
from fastapi import (
    APIRouter,
    Request, Depends, Form, HTTPException,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi import Response

from ..dependencies import get_db_session, login_user, get_user_from_session, oauth
from ..models.user import User
from ..utils.errors.errors import UserDataError, OauthProviderError
from ..utils.additional_func_auth import hash_password, pwd_context
from ..utils.enums import OauthProvider
from ..utils.errors.error_messages import OAUTH_NO_EMAIL, OAUTH_NO_USER_INFO, PASSWORD_REQUIRED, PASSWORDS_DO_NOT_MATCH, \
    EMAIL_ALREADY_REGISTERED, GOOGLE_USER, USER_NOT_FOUND, INCORRECT_PASSWORD

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter()

#Gets register template
@router.get("/register", tags=["auth"], response_class=HTMLResponse)
async def register_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("register.html", {"request": request})


#Post view for user registration
@router.post("/register", tags=["auth"], response_class=HTMLResponse)
async def register_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()],
        db: Session = Depends(get_db_session)) -> RedirectResponse:

    if not password:
        return HTMLResponse(content=PASSWORD_REQUIRED, status_code=400)

    if password != confirm_password:
        return HTMLResponse(content=PASSWORDS_DO_NOT_MATCH, status_code=400)

    hashed_password = hash_password(password)
    try:
        new_user = User(email=email,
                        password=hashed_password,
                        oauth_provider=OauthProvider.ORDINARY_USER
                        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse(url="/login", status_code=303)
    except IntegrityError:
        db.rollback()
        return HTMLResponse(content=EMAIL_ALREADY_REGISTERED, status_code=400)

    return RedirectResponse(url="/login", status_code=303)


#Gets login template
@router.get("/login", tags=["auth"], response_class=HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("/login.html", {"request": request})

#Post view for user login
@router.post("/login", tags=["auth"], response_class=HTMLResponse)
async def login(
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: Session = Depends(get_db_session)) -> Response:

        user = User.get_by_email(db, email)
        if not user:
            return HTMLResponse(content=USER_NOT_FOUND, status_code=400)
        if user.oauth_provider == OauthProvider.GOOGLE:
            return HTMLResponse(content=GOOGLE_USER, status_code=400)
        if not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=400, detail=INCORRECT_PASSWORD)
        user_data = {"id": user.id, "email": user.email}
        response = login_user(user=user_data, redirect_url="/get_authenticated_page")
        return response

#For now it returns page for authenticated person
@router.get("/get_authenticated_page", tags=["auth"], response_class=HTMLResponse)
async def get_authenticated_page(
        request: Request,
        db: Session = Depends(get_db_session)
) -> HTMLResponse:
    # Get the session cookie
    cookie_value = request.cookies.get("sess")
    if not cookie_value:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Retrieve the user from the session
    user = get_user_from_session(cookie_value, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session or user does not exist")

    # Pass the user to the template
    return templates.TemplateResponse("/authenticated_index.html", {"request": request, "user": user})


@router.get("/logout")
async def logout(request: Request, response: Response) -> Response:
    response = RedirectResponse(url="/")
    response.delete_cookie(key="sess")
    return response


#Google Authentication
def oauth_user(email: str, oauth_provider: OauthProvider,  session: Session):

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
        user = oauth_user(
            email=email,
            session=session,
            oauth_provider=OauthProvider.GOOGLE
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = login_user(user=user, redirect_url="get_authenticated_page")
    return response
