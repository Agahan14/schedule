import os
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from ..dependencies import get_db_session, get_current_user
from ..models import Event


current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/event")


@router.get("/create", tags=["event"], response_class=HTMLResponse)
async def get_create_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("create_event.html", {"request": request})


@router.post("/create", tags=["event"], response_class=HTMLResponse)
async def create(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    url: Annotated[str, Form()],
    duration: Annotated[int, Form()],
    session: Session = Depends(get_db_session),
):
    current_user = get_current_user(request=request, session=session)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_event = Event(
        user_id=current_user.id,
        title=title,
        location_url=None,
        description=description,
        url=url,
        duration=duration,
    )
    session.add(db_event)
    session.commit()
    session.refresh(db_event)

    return RedirectResponse(url="/event", status_code=303)


@router.get("/", tags=["event"])
async def events(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    events = Event.get_all_by_user_id(session, current_user.id)
    if not current_user:
        raise HTTPException(status_code=401)
    return templates.TemplateResponse(
        "event.html",
        {"request": request, "events": events},
    )


@router.get("/update/{event_id}", tags=["event"])
async def get_update_form(request: Request, event_id: int, session: Session = Depends(get_db_session)):
    event = Event.get_by_id(session, event_id=event_id)
    return templates.TemplateResponse("update_event.html", {"request": request, "event_id": event_id, "event": event})


@router.post("/update/{event_id}", tags=["event"], response_class=HTMLResponse)
async def event(
    request: Request,
    event_id: int,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    url: Annotated[str, Form()] = None,
    duration: Annotated[int, Form()] = None,
    session: Session = Depends(get_db_session),
):
    current_user = get_current_user(request=request, session=session)

    if not current_user:
        raise HTTPException(status_code=401)

    event = Event.get_by_id(session, event_id=event_id)
    if not event and event.user_id == current_user:
        raise HTTPException(status_code=404, detail="Event not found.")

    if title:
        event.title = title
    if description:
        event.description = description
    if url:
        event.url = url
    if duration:
        event.duration = duration

    session.add(event)
    session.commit()
    session.refresh(event)

    return RedirectResponse(url=f"/event/update/{event_id}", status_code=303)
