from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..dependencies import get_db_session, templates
from ..models import Event, User

router = APIRouter(prefix="/host")


@router.get(f"/{str}", tags=["host"])
async def get_host_events(username: str, request: Request, session: Session = Depends(get_db_session)):
    user = User.get_by_username(session=session, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_name = user.full_name

    picture_url = user.picture_url

    events = Event.get_all_by_user_id(session, user.id)
    return templates.TemplateResponse(
        "host_events.html",
        {
            "request": request,
            "username": user_name,
            "user_pic": picture_url,
            "events": events,
        },
    )


@router.get("/s", tags=["host"])
async def get_event_booking(request: Request, session: Session = Depends(get_db_session)):
    user = User.get_by_username(session=session, username="Micheal-Jackson")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    event = Event.get_by_id(session, 1)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.user_id != user.id:
        raise HTTPException(status_code=404, detail="User's event not found")

    user_name = user.full_name
    if user.picture_url:
        picture_url = user.picture_url
    else:
        picture_url: str = "/static/images/profile_pictures/profile_picture.jpg"

    return templates.TemplateResponse(
        "host/booking_event.html",
        {
            "request": request,
            "username": user_name,
            "user_pic": picture_url,
            "event": event,
        },
    )
