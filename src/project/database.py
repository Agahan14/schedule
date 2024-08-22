import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("_SC_DATABASE_URL", "sqlite:///db.sqlite")
if DATABASE_URL == "":
    DATABASE_URL = "sqlite:///db.sqlite"

ECHO = os.getenv("APP_ENV") != "PROD"
POOL_RECYCLE = 1800
POOL_SIZE = 5


engine = create_engine(
    DATABASE_URL,
    echo=ECHO,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=True,
    pool_size=POOL_SIZE,
)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def lifespan(application: FastAPI):
    if os.getenv("APP_ENV") != "PROD":
        with engine.begin() as conn:
            Base.metadata.create_all(conn)

    yield
