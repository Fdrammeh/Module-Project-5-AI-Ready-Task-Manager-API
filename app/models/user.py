# project/starter/app/models/user.py
# Module 5 Project — User model
#
# TODO: Define the User ORM model
# Fields: id, username (unique), email (unique), hashed_password
# Relationship: one user has many tasks

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # TODO: Add columns
    # TODO: Add relationship to Task (tasks = relationship("Task", back_populates="owner"))
    pass
    id:Mapped [int] = mapped_column(primary_key=True, index=True)
    username:Mapped[str]=mapped_column(String, unique=True, nullable=False, index=True)
    email:Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")