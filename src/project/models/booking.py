from __future__ import annotations

import datetime
from collections.abc import Sequence

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    desc,
    func,
    select,
)
from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    Session,
    mapped_column,
    relationship,
)

from ..database import Base
from .event import Event


class Booking(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, init=False
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=None
    )
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_canceled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("event.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
        init=False,
    )
    # NOTE Decide how to implement additional notes for bookings from events
    # additional_notes: Mapped[list[str]] = mapped_column(
    #     String, nullable=True, init=False
    # )
    
    event: Mapped["Event"] = relationship(
        "Event", back_populates="bookings", default=False
    )

    @staticmethod
    def delete_by_id(session_shedule: Session, id: int) -> None:
        if booking := Booking.get_by_id(session_shedule=session_shedule, id=id):
            session_shedule.delete(booking)
            session_shedule.commit()

    @staticmethod
    def get_by_id(session_shedule: Session, id: int) -> Booking | None:
        return session_shedule.scalar(select(Booking).where(Booking.id == int(id)))

    @staticmethod
    def get_all_by_user_id(
        session_shedule: Session, user_id: int
    ) -> Sequence[Booking] | None:
        return session_shedule.scalars(
            select(Booking)
            .where(
                Booking.event_id.in_(select(Event.id).where(Event.user_id == user_id))
            )
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_canceld_by_user_id(
        session_shedule: Session, user_id: int
    ) -> Sequence[Booking] | None:
        return session_shedule.scalars(
            select(Booking)
            .where(Booking.event_id.user_id == user_id, Booking.is_canceled._is(True))
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_unconfirmed_by_user_id(
        session_shedule: Session, user_id: int
    ) -> Sequence[Booking] | None:
        return session_shedule.scalars(
            select(Booking)
            .where(Booking.event_id.user_id == user_id, Booking.is_confirmed._is(False))
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_upcoming_by_user_id(
        session_shedule: Session, user_id: int
    ) -> Sequence[Booking] | None:
        return session_shedule.scalars(
            select(Booking)
            .where(
                Booking.event_id.user_id == user_id, Booking.date > func.current_time()
            )
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_past_bookings_by_user_id(
        session_shedule: Session, user_id: int
    ) -> Sequence[Booking] | None:
        return session_shedule.scalars(
            select(Booking)
            .where(
                Booking.event_id.user_id == user_id, Booking.date < func.current_time()
            )
            .order_by(desc(Booking.created_at))
        ).all()
