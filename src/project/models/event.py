from __future__ import annotations

import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    select,
    sql,
)
from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    Session,
    mapped_column,
)

from ..database import Base


class Event(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        init=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    location_url: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, init=False
    )
    is_hidden: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=sql.false(), init=False
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    description: Mapped[str] = mapped_column(String, nullable=True, default=None)

    @staticmethod
    def get_by_id(session: Session, event_id: int) -> Event | None:
        return session.scalar(select(Event).where(Event.id == event_id))
