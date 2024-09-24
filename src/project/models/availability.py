from __future__ import annotations

from sqlalchemy import (
    JSON,
    Boolean,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, MappedAsDataclass, Session, backref, mapped_column, relationship

from ..database import Base

# class WorkSchedule(MappedAsDataclass, Base):
#     __tablename__ = "work_schedule"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     availability_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("availability.id", ondelete="CASCADE"), nullable=False
#     )
#     work_schedule: Mapped[dict] = mapped_column(JSON, nullable=True)
#     availability = relationship("Availability", backref=backref("work_schedules", passive_deletes=True))
#


class Availability(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "availability"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    # schedule: Mapped[List[WorkSchedule]] = relationship(
    #     "WorkSchedule", back_populates="availability", cascade="all, delete-orphan"
    # )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        init=False,
    )
    user: Mapped["User"] = relationship(  # type: ignore # noqa
        "User", backref=backref("availabilities", cascade="all, delete-orphan")
    )
    work_schedule: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @staticmethod
    def get_by_id(session: Session, id: int) -> Availability | None:
        return session.scalar(select(Availability).where(Availability.id == int(id)))

    @staticmethod
    def get_user_availability(session: Session, aval_id: int, user_id: int) -> Availability | None:
        return session.scalar(
            select(Availability).where(Availability.id == int(aval_id), Availability.user_id == user_id)
        )


# class EventLimit(MappedAsDataclass, unsafe_hash=True):
#     __tablename__ = "event_limit"
#
#     id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
#     # time_limit:
#     minimum_notice_time_type: Mapped[TimeType] = mapped_column(
#         Enum(TimeType), nullable=False
#     )
#     minimum_notice: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
#     event_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey("event.id", ondelete="CASCADE"),
#         nullable=False,
#         unique=False,
#         init=False,
#     )
#     start_time: Mapped[int] = mapped_column(
#         Integer,
#         init=False,
#         constraint=CheckConstraint(
#             "start_time >= 0 AND start_time <= 120 AND start_time % 5 = 0",
#             name="check_start_time",
#         ),
#     )
#     end_time: Mapped[int] = mapped_column(
#         Integer,
#         init=False,
#         constraint=CheckConstraint(
#             "end_time >= 0 AND end_time <= 120 AND end_time % 5 = 0",
#             name="check_end_time",
#         ),
#     )
#     interval: Mapped[int] = mapped_column(
#         Integer,
#         init=False,
#         primary_key=True,
#         constraint=CheckConstraint(
#             "interval >= 0 AND interval <= 120 AND interval % 5 = 0",
#             name="check_interval",
#         ),
#     )
