import os
from typing import Annotated

from fastapi import (
    APIRouter,
    Request, Depends, Form, HTTPException,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, HTMLResponse

from ..dependencies import get_db_session, login_user, get_user_from_session
from ..models.user import User
from ...utils import hash_password, pwd_context
from fastapi import Response

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)
router = APIRouter(prefix="/auth")


#Gets register template
@router.get("/register", tags=["auth"], response_class=HTMLResponse)
async def get_register_user(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("register.html", {"request": request})


#Post view for user registration
@router.post("/register", tags=["auth"], response_class=HTMLResponse)
async def post_register_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()],
        db: Session = Depends(get_db_session)) -> RedirectResponse:
    if password != confirm_password:
        return HTMLResponse(content="Passwords do not match.", status_code=400)
    hashed_password = hash_password(password)
    try:
        new_user = User(email=email,
                        password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        return HTMLResponse(content="Email already registered.", status_code=400)
    return RedirectResponse(url="/auth/login", status_code=303)


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
    try:
        user = User.get_by_email(db, email)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    response = login_user(user=user, redirect_url="/auth/get_authenticated_page")
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