import os
from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from ..dependencies import get_current_user, get_db_session
from ..models import Booking

router = APIRouter(prefix="/booking")

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dirs = [
    os.path.join(current_dir, "..", "templates/booking"),
    os.path.join(current_dir, "..", "templates/components"),
]

templates = Jinja2Templates(directory=template_dirs)


@router.get("/upcoming", tags=["booking"])
async def upcoming(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_upcoming_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "upcoming.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,
        },
    )


@router.get("/unconfirmed", tags=["booking"])
async def uncomfirmed(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_unconfirmed_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "unconfirmed.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,
        },
    )


@router.get("/canceled", tags=["booking"])
async def canceled(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_canceled_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "canceled.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,
        },
    )


@router.get("/past", tags=["booking"])
async def past(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_past_bookings_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "past.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,
        },
    )
