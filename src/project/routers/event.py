import requests
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from ..dependencies import get_db_session, templates
from ..models import Event

router = APIRouter(prefix="/event")


@router.get("/event", tags=["event"])
async def academy(request: Request, session: Session = Depends(get_db_session)):
    events = Event.get_all(session)
    return templates.TemplateResponse(
        "event.html",
        {"request": request, "events": events},
    )
