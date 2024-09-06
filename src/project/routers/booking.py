import os
from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from ..dependencies import get_current_user, get_db_session
from ..models import Booking

router = APIRouter(prefix="/booking")

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)


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
