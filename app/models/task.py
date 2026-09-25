# project/starter/app/models/task.py
# Module 5 Project — Task model
#
# TODO: Define the Task ORM model
# Fields: id, title, description (optional), completed (bool, default False), owner_id (FK)
# Relationship: task belongs to a user

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # TODO: Add columns
    # TODO: Add owner_id ForeignKey to users.id
    # TODO: Add relationship to User (owner = relationship("User", back_populates="tasks"))
    pass
    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    title: Mapped[str]= mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates ="tasks")

    