from typing import Optional

from sqlalchemy import Column, String, Integer, select
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column, Session
from sqlalchemy.testing.pickleable import User

from src.project.database import Base
from collections.abc import Sequence


class User(MappedAsDataclass, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    email: str = mapped_column(String(255), unique=True, nullable=False)
    password: str = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    @staticmethod
    def get_by_id(session_schedule: Session, id: int) -> User | None:
        return session_schedule.scalar(select(User).where(User.id == int(id)))


    @staticmethod
    def get_by_email(session_schedule: Session, email: str) -> User | None:
        return session_schedule.scalar(select(User).where(User.email == email))

    @staticmethod
    def get_all(session_schedule: Session) -> Sequence[User]:
        return (session_schedule.scalars(select(User))).all()
