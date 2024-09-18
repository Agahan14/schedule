from __future__ import annotations
from collections.abc import Sequence

from sqlalchemy import Boolean, Integer, String, select, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, MappedAsDataclass, Session, mapped_column
from sqlalchemy import Enum as SQLEnum
from ..database import Base
from ..utils.enums import OauthProvider


class User(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    oauth_provider: Mapped[OauthProvider] = mapped_column(SQLEnum(OauthProvider))
    email: str = mapped_column(String(255), unique=True, nullable=True)
    password: str = mapped_column(String(255), nullable=True, default=None)
    username: Mapped[str] = mapped_column(
        String, nullable=True, unique=True, default=None
    )
    picture_url: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    about: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)


    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

    @staticmethod
    def get_all(session: Session) -> Sequence[User]:
        return (session.scalars(select(User))).all()

    @staticmethod
    def get_by_id(session: Session, id: int) -> User | None:
        return session.scalar(select(User).where(User.id == int(id)))

    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        return session.scalar(select(User).where(User.email == email))

    @staticmethod
    def delete(session: Session, id: int) -> User | None:
        try:
            user = session.scalar(select(User).where(User.id == id))
            if user:
                session.delete(user)
                session.commit()
                return user
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {str(e)}")  # You can replace this with proper logging
            return None


    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
