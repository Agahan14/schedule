import os

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.project.dependencies import get_current_user, get_db_session
from src.project.models import Availability

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter()


@router.get("/availability", tags=["availability"], response_class=HTMLResponse)
async def get_availability(request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    current_user = get_current_user(request, session)
    return templates.TemplateResponse("availability.html", {"request": request, "user": current_user})


@router.api_route(
    "/availability_detail/{id}", methods=["GET", "POST"], tags=["availability"], response_class=HTMLResponse
)
async def availability_detail(id: int, request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    if request.method == "GET":
        current_user = get_current_user(request, session)
        availability = Availability.get_user_availability(session, aval_id=id, user_id=current_user.id)
        return templates.TemplateResponse(
            "availability_detail.html", {"request": request, "user": current_user, "availability": availability}
        )
    elif request.method == "POST":
        current_user = get_current_user(request, session)
        work_schedule = await request.json()
        availability = Availability.get_user_availability(session, aval_id=id, user_id=current_user.id)
        availability.work_schedule = work_schedule
        session.commit()
        return templates.TemplateResponse(
            "availability_detail.html", {"request": request, "user": current_user, "availability": availability}
        )
