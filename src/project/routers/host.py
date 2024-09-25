from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..dependencies import get_db_session, templates
from ..models import Event, User

router = APIRouter(prefix="/host")


@router.get("/{username}", tags=["host"])
async def get_host_events(username: str, request: Request, session: Session = Depends(get_db_session)):
    user = User.get_by_username(session=session, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_name = user.full_name

    events = Event.get_all_by_username(session, user_name)
    return templates.TemplateResponse(
        "host_events.html",
        {
            "request": request,
            "username": user_name,
            "events": events,
        },
    )


@router.get("/{username}/{eventId}", tags=["host"])
async def get_event_booking(username: str, eventId: int, request: Request, session: Session = Depends(get_db_session)):  # noqa: N803
    user = User.get_by_username(session=session, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    event = Event.get_by_id(session, eventId)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.user_id != user.id:
        raise HTTPException(status_code=404, detail="User's event not found")

    user_name = user.full_name
    if user.picture_url:
        picture_url = user.picture_url
    else:
        picture_url = "/static/images/profile_pictures/profile_picture.jpg"

    return templates.TemplateResponse(
        "host/booking_event.html",
        {
            "request": request,
            "username": user_name,
            "user_pic": picture_url,
            "event": event,
        },
    )
