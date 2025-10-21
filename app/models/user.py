from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from app.db.session import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
	full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

	transactions: Mapped[List["Transaction"]] = relationship(
		"Transaction", back_populates="owner", cascade="all, delete-orphan"
	)
