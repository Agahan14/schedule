# noinspection PyInterpreter
import os
from typing import Annotated

from fastapi import (
    APIRouter,
    Request, Depends, Form,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, HTMLResponse

from src.project.dependencies import get_db_session
from src.project.models.user import User

router = APIRouter()
current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)


@router.get("/")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

