from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric
from decimal import Decimal
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.weight import Weight
    from app.models.transaction import Transaction

class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    shortname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False, default=Decimal('0.000'))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"), index=True, nullable=False)
    weight_id: Mapped[int] = mapped_column(ForeignKey("weights.id", ondelete="RESTRICT"), index=True, nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="inventory_items")
    weight: Mapped["Weight"] = relationship("Weight", back_populates="inventory_items")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="inventory")
