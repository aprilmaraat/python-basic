from __future__ import annotations
from datetime import date
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Date
from app.db.session import Base


class TransactionType(str, Enum):
	expense = "expense"
	earning = "earning"
	capital = "capital"

class Transaction(Base):
	__tablename__ = "transactions"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
	description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
	transaction_type: Mapped[TransactionType] = mapped_column(default=TransactionType.expense, nullable=False)
	amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
	date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

	owner: Mapped["User"] = relationship("User", back_populates="transactions")
