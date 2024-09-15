import os
from datetime import datetime

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
from sqlalchemy.orm import session, Session
from sqlalchemy.sql.functions import count
from starlette.responses import HTMLResponse

from starlette.templating import Jinja2Templates

from src.project.dependencies import get_current_user, get_db_session

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter()

@router.get("/availability", tags=["availability"], response_class=HTMLResponse)
async def get_availability(request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    current_user = get_current_user(request, session)
    return templates.TemplateResponse("availability.html", {"request": request, "user": current_user})


