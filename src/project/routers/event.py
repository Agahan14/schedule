import os

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from ..dependencies import get_db_session
from ..models import Event



current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/event")


@router.get("/", tags=["event"])
async def events(request: Request, session: Session = Depends(get_db_session)):
    events = Event.get_all(session)
    return templates.TemplateResponse(
        "event.html",
        {"request": request, "events": events},
    )




