from sqlalchemy import String, Integer, select, Boolean
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column, Session
from sqlalchemy.testing.pickleable import User
from collections.abc import Sequence
from ..database import Base


class User(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    email: str = mapped_column(String(255), unique=True, nullable=False)
    password: str = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    picture_url: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    @staticmethod
    def get_all(session_schedule: Session) -> Sequence[User]:
        return (session_schedule.scalars(select(User))).all()

    @staticmethod
    def get_by_id(session_schedule: Session, id: int) -> User | None:
        return session_schedule.scalar(select(User).where(User.id == int(id)))

    @staticmethod
    def get_by_email(session_schedule: Session, email: str) -> User | None:
        return session_schedule.scalar(select(User).where(User.email == email))

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
