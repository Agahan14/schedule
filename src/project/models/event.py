from __future__ import annotations

import datetime
from collections.abc import Sequence

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    desc,
    func,
    select,
    sql,
)
from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    Session,
    mapped_column,
    relationship,
)

from src.project.utils.enums import BookingStatus, TimeType

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
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="event", cascade="all, delete-orphan")
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    location_url: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, init=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sql.false(), init=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    time_type: Mapped[TimeType] = mapped_column(Enum(TimeType), nullable=True, init=False, default=TimeType.MINUTES)
    description: Mapped[str] = mapped_column(String, nullable=True, default=None)

    @staticmethod
    def get_by_id(session: Session, event_id: int) -> Event | None:
        return session.scalar(select(Event).where(Event.id == event_id))

    @staticmethod
    def get_all(session: Session) -> Sequence[Event] | None:
        return (session.scalars(select(Event))).all()

    @staticmethod
    def get_all_by_user_id(session: Session, user_id: int) -> Sequence[Event] | None:
        return session.scalars((
            select(Event).where(Event.user_id == user_id)).order_by(Event.date)).all()


class Booking(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, init=False
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=None)
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

    event: Mapped[Event] = relationship("Event", back_populates="bookings", default=False)

    @staticmethod
    def delete_by_id(session: Session, id: int) -> None:
        if booking := Booking.get_by_id(session=session, id=id):
            session.delete(booking)
            session.commit()

    @staticmethod
    def get_by_id(session: Session, id: int) -> Booking | None:
        return session.scalar(select(Booking).where(Booking.id == int(id)))

    @staticmethod
    def get_all_by_user_id(session: Session, user_id: int) -> Sequence[Booking] | None:
        return session.scalars(
            select(Booking)
            .where(Booking.event_id.in_(select(Event.id).where(Event.user_id == user_id)))
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_canceld_by_user_id(session: Session, user_id: int) -> Sequence[Booking] | None:
        return session.scalars(
            select(Booking)
            .join(Event)
            .where(Event.user_id == user_id, Booking.status.is_(BookingStatus.CANCELED))
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_unconfirmed_by_user_id(session: Session, user_id: int) -> Sequence[Booking] | None:
        return session.scalars(
            select(Booking)
            .join(Event)
            .where(
                Event.user_id == user_id,
                Booking.date > func.current_time(),
                Booking.status.is_(BookingStatus.UNCONFIRMED),
            )
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_upcoming_by_user_id(session: Session, user_id: int) -> Sequence[Booking] | None:
        return session.scalars(
            select(Booking)
            .where(Booking.event_id.user_id == user_id, Booking.date > func.current_time())
            .order_by(desc(Booking.created_at))
        ).all()

    @staticmethod
    def get_all_past_bookings_by_user_id(session: Session, user_id: int) -> Sequence[Booking] | None:
        return session.scalars(
            select(Booking)
            .where(Booking.event_id.user_id == user_id, Booking.date < func.current_time())
            .order_by(desc(Booking.created_at))
        ).all()
