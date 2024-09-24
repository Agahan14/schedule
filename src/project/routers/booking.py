from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db_session, templates
from ..models import Booking
from ..utils.enums import BookingStatus

router = APIRouter(prefix="/booking")


@router.get("/")
async def index(request: Request, session: Session = Depends(get_db_session)):
    return RedirectResponse(url="booking/upcoming", status_code=301)


@router.get("/info/{id}", tags=["booking"])
async def book_information(id: int, request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    booking = Booking.get_by_id(session, id=id)
    formated_date = booking.date.strftime("%A, %B %d, %Y")  # type: ignore
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return templates.TemplateResponse(
        "booking/book_information.html",
        {
            "request": request,
            "user": current_user,
            "booking": booking,
            "timedelta": timedelta,
            "formated_date": formated_date,
        },
    )


@router.get("/upcoming", tags=["booking"])
async def upcoming(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_upcoming_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "booking/upcoming.html",
        {
            "request": request,
            "user": current_user,
            "bookings": bookings,
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
        "booking/unconfirmed.html",
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
        "booking/canceled.html",
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
        "booking/past.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,
        },
    )


@router.post(f"/booking/cancel/{id}", tags=["booking"])
async def cancel(booking_id: int, request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=404, detail="User not found.")

    booking = Booking.get_by_id(session, id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")

    if booking.event.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are not allowed to cancel this meeting.")

    booking.status = BookingStatus.CANCELED

    session.commit()
    session.refresh(booking)


@router.delete(f"/booking/delete/{id}", tags=["booking"])
async def delete_booking(booking_id: int, request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    booking = session.get(Booking, booking_id)
    if not booking or booking.event.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found or you are not allowed to cancel this meeting.")

    if booking.status not in (BookingStatus.CANCELED, BookingStatus.PAST):
        raise HTTPException(status_code=401, detail="You are not allowed to cancel this meeting.")

    session.delete(booking)
    session.commit()
