from typing import Optional

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column

from src.project.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
