import os

from fastapi import APIRouter, Depends, Request
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from ..dependencies import get_db_session, get_current_user
from ..models import Event

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/event")


@router.get("/", tags=["event"])
async def events(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    events = Event.get_all_by_user_id(session, current_user.id)
    return templates.TemplateResponse(
        "event.html",
        {"request": request, "events": events},
    )


@router.get("/{id}/", tags=["event"])
async def get_event(id: int, request: Request, session: Session = Depends(get_db_session)):
    event = Event.get_by_id(session, id)
    return templates.TemplateResponse("retrieve_event.html", {"request": request, "event": event})
