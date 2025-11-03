from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Date, Numeric
from sqlalchemy.ext.hybrid import hybrid_property
from decimal import Decimal
from app.db.session import Base

if TYPE_CHECKING:
	from app.models.user import User
	from app.models.inventory import Inventory


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
	# Renamed logically from 'amount' to 'amount_per_unit'; keep underlying column name 'amount' for backward compatibility.
	amount_per_unit: Mapped[Decimal] = mapped_column('amount', Numeric(10, 2), default=Decimal('0.00'), nullable=False)
	quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
	inventory_id: Mapped[Optional[int]] = mapped_column(ForeignKey("inventory.id", ondelete="SET NULL"), index=True, nullable=True)
	date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

	owner: Mapped["User"] = relationship("User", back_populates="transactions")
	inventory: Mapped[Optional["Inventory"]] = relationship("Inventory", back_populates="transactions")

	@hybrid_property
	def total_amount(self) -> Decimal:
		return (self.amount_per_unit or Decimal('0.00')) * (self.quantity or 0)

	@total_amount.expression
	def total_amount(cls):  # type: ignore[override]
		return cls.amount_per_unit * cls.quantity
