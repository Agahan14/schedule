from typing import List
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String, JSON,
)

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship, backref

from ..database import Base


class WorkSchedule(MappedAsDataclass, Base):
    __tablename__ = "work_schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    availability_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("availability.id", ondelete="CASCADE"), nullable=False
    )
    work_schedule: Mapped[dict] = mapped_column(JSON, nullable=True)
    availability = relationship("Availability", backref=backref("events", passive_deletes=True))


class Availability(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "availability"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    schedule: Mapped[List[WorkSchedule]] = relationship(
        "WorkSchedule", back_populates="availability", cascade="all, delete-orphan"
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        init=False,
    )
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("event.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        init=False,
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)




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


