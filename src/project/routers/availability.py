import json

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from ..dependencies import current_dir, get_current_user, get_db_session, template_dir, templates
from ..models import Availability
from ..utils.enums import default_work_schedule

current_dir = current_dir
template_dir = template_dir
templates = templates

router = APIRouter()


@router.get("/availability", tags=["availability"], response_class=HTMLResponse)
async def get_availability(request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    current_user = get_current_user(request, session)
    return templates.TemplateResponse("availability/list_availability.html", {"request": request, "user": current_user})


@router.post("/create_availability", tags=["availability"], response_class=HTMLResponse)
async def create_availability(request: Request, session: Session = Depends(get_db_session)) -> RedirectResponse:
    current_user = get_current_user(request, session)
    body = await request.json()
    name = body.get('name')
    work_schedule = default_work_schedule
    new_availability = Availability(name=name, user=current_user, work_schedule=work_schedule, is_default=False)

    session.add(new_availability)
    session.commit()
    availability_id = new_availability.id

    return RedirectResponse(url=f"/availability/{availability_id}", status_code=303)



@router.api_route("/availability/{id}", methods=["GET", "POST"], tags=["availability"], response_class=HTMLResponse)
async def availability_detail(id: int, request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    if request.method == "GET":
        current_user = get_current_user(request, session)
        availability = Availability.get_user_availability(session, aval_id=id, user_id=current_user.id)
        print(availability.id)
        availability_data = {
            "name": availability.name,
            "is_default": availability.is_default,
            "work_schedule": [
                {
                    "day_of_week": ws.get("day_of_week"),
                    "time_from": ws.get("time_from"),
                    "time_to": ws.get("time_to"),
                    "is_active": ws.get("is_active")
                } for ws in availability.work_schedule
            ]
        }
        return templates.TemplateResponse(
            "availability/availability_detail.html",
            {"request": request, "user": current_user, "availability": availability_data})
    elif request.method == "POST":
        current_user = get_current_user(request, session)
        work_schedule = await request.json()
        availability = Availability.get_user_availability(session, aval_id=id, user_id=current_user.id)
        availability.work_schedule = work_schedule
        session.commit()
        return templates.TemplateResponse(
            "availability/availability_detail.html",
            {"request": request, "user": current_user, "availability": availability},
        )
