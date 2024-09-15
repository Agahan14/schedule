import os
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from pydantic import BaseModel
from starlette import responses, status
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from ..dependencies import get_db_session, get_current_user
from ..models import Event



current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/event")


@router.get("/", tags=["event"])
async def events(request: Request, session: Session = Depends(get_db_session)):
    current_user = get_current_user(request=request, session=session)
    events = Event.get_all_by_user_id(session, current_user.id)
    return templates.TemplateResponse(
        "event.html",
        {"request": request, "events": events},
    )


# @router.get("/{id}/", tags=["event"])
# async def get_event(id: int, request: Request, session: Session = Depends(get_db_session)):
#     event = Event.get_by_id(session, id)
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return templates.TemplateResponse("update_event.html", {"request": request, "event": event})


@router.post("/create/", tags=["event"], response_class=responses.HTMLResponse)
async def create_event(
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
    return responses.RedirectResponse(url="/event/", status_code=303)
