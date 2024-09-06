# noinspection PyInterpreter
import os

from fastapi import (
    APIRouter,
    Request,
)
from fastapi.templating import Jinja2Templates
router = APIRouter()
current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)


@router.get("/")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

