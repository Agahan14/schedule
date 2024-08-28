from __future__ import annotations

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select
 
)


from sqlalchemy.orm import (
    Mapped,
    MappedAsDataclass,
    Session,
    mapped_column
)

from ..database import Base


class User(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "user"
  
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    picture_url: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    username : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    

    @staticmethod
    def get_by_user_id(session: Session, user_id: int) -> User | None:
        return session.scalar(select(User).where(User.user_id == user_id))
  

