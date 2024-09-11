# noinspection PyInterpreter
import os

from fastapi import (
    APIRouter,
    Request, Depends,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db_session

router = APIRouter()
current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)


@router.get("/")  # Adjust the route as needed
async def main(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request, session)
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})
