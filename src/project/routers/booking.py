from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db_session, templates
from ..models.booking import Booking

router = APIRouter(prefix="/booking")


@router.get("/", tags=["booking"])
async def booking(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    bookings = Booking.get_all_by_user_id(session, user_id=1)
    return templates.TemplateResponse(
        "booking.html",
        {
            "request": request,
            "bookings": bookings,
            "user": current_user,
            "timedelta": timedelta,  # temporary fix
        },
    )
