from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from ..dependencies import get_current_user, get_db_session, templates
from ..models import Event

router = APIRouter(prefix="/event")


@router.get("/create", tags=["event"], response_class=HTMLResponse)
async def get_create_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("event/create_event.html", {"request": request})


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
async def events(request: Request, page: int = Query(1, ge=1), session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)

    if not current_user:
        raise HTTPException(status_code=401)

    page_size = 5
    offset = (page - 1) * page_size

    page_range = range(1, 5)

    events = Event.get_all_by_user_id(session, current_user.id, limit=page_size, offset=offset)

    total_items = Event.count_events_by_user_id(session, current_user.id)

    total_pages = (total_items + page_size - 1) // page_size

    page_range = range(1, total_pages + 1)

    return templates.TemplateResponse(
        "event/event.html",
        {
            "request": request,
            "events": events,
            "page": page,
            "per_page": page_size,
            "total_pages": total_pages,
            "total_items": total_items,
            "page_range": page_range,
        },
    )


@router.get("/update/{event_id}", tags=["event"])
async def get_update_form(request: Request, event_id: int, session: Session = Depends(get_db_session)):
    event = Event.get_by_id(session, event_id=event_id)
    return templates.TemplateResponse(
        "event/update_event.html", {"request": request, "event_id": event_id, "event": event}
    )


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
    if not event or event.user_id == current_user:
        raise HTTPException(status_code=404, detail="Event not found.")

    fields_to_update = {"title": title, "description": description, "url": url, "duration": duration}

    for field, value in fields_to_update.items():
        if value is not None:
            setattr(event, field, value)

    session.add(event)
    session.commit()
    session.refresh(event)

    return RedirectResponse(url="/event", status_code=303)
