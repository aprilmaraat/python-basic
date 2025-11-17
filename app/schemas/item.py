from pydantic import BaseModel, Field, field_validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from app.models.transaction import TransactionType
from app.core.timezone import now_philippines

if TYPE_CHECKING:
	from app.schemas.user import UserReadSimple
	from app.schemas.inventory import InventoryReadSimple


class TransactionBase(BaseModel):
	title: str
	description: Optional[str] = None
	transaction_type: TransactionType = TransactionType.expense
	amount_per_unit: Decimal = Decimal('0.00')
	quantity: Decimal = Decimal('1.000')
	purchase_price: Decimal = Decimal('0.00')
	date: datetime  # No default - must be explicitly provided

	@field_validator("amount_per_unit", "purchase_price", mode="before")
	def to_decimal_money(cls, v):  # type: ignore[override]
		if isinstance(v, (int, float, str)):
			return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
		return v
	
	@field_validator("quantity", mode="before")
	def to_decimal_quantity(cls, v):  # type: ignore[override]
		if isinstance(v, (int, float, str)):
			return Decimal(str(v)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
		return v


class TransactionCreate(TransactionBase):
	owner_id: int
	inventory_id: Optional[int] = None
	date: datetime = Field(default_factory=now_philippines)  # Default to Philippines time (GMT+8)

	@field_validator("date", mode="before")
	def ensure_naive_datetime(cls, v):  # type: ignore[override]
		"""Ensure date is a naive datetime (no timezone info) representing local time"""
		if v is None:
			return now_philippines()
		if isinstance(v, str):
			# Parse string to datetime - will be naive
			return datetime.fromisoformat(v.replace('Z', '+00:00')).replace(tzinfo=None)
		if isinstance(v, datetime):
			# If timezone-aware, convert to local time and remove tzinfo
			if v.tzinfo is not None:
				# Remove timezone info to store as naive datetime
				return v.replace(tzinfo=None)
			return v
		return v


class TransactionUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	transaction_type: Optional[TransactionType] = None
	amount_per_unit: Optional[Decimal] = None
	quantity: Optional[Decimal] = None
	purchase_price: Optional[Decimal] = None
	date: Optional[datetime] = None
	inventory_id: Optional[int] = None

	@field_validator("amount_per_unit", "purchase_price", mode="before")
	def to_decimal_money(cls, v):  # type: ignore[override]
		if v is None:
			return v
		if isinstance(v, (int, float, str)):
			return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
		return v
	
	@field_validator("quantity", mode="before")
	def to_decimal_quantity(cls, v):  # type: ignore[override]
		if v is None:
			return v
		if isinstance(v, (int, float, str)):
			return Decimal(str(v)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
		return v

	@field_validator("date", mode="before")
	def ensure_naive_datetime_update(cls, v):  # type: ignore[override]
		"""Ensure date is a naive datetime (no timezone info) representing local time"""
		if v is None:
			return None
		if isinstance(v, str):
			# Parse string to datetime - will be naive
			return datetime.fromisoformat(v.replace('Z', '+00:00')).replace(tzinfo=None)
		if isinstance(v, datetime):
			# If timezone-aware, convert to local time and remove tzinfo
			if v.tzinfo is not None:
				# Remove timezone info to store as naive datetime
				return v.replace(tzinfo=None)
			return v
		return v


class TransactionRead(BaseModel):
	id: int
	title: str
	description: Optional[str]
	owner_id: int
	transaction_type: TransactionType
	amount_per_unit: Decimal
	quantity: Decimal
	purchase_price: Decimal
	total_amount: Decimal
	date: datetime
	inventory_id: Optional[int]

	model_config = {"from_attributes": True}


class TransactionReadSimple(BaseModel):
	id: int
	title: str
	description: Optional[str]
	owner_id: int
	transaction_type: TransactionType
	amount_per_unit: Decimal
	quantity: Decimal
	purchase_price: Decimal
	total_amount: Decimal
	date: datetime
	inventory_id: Optional[int]

	model_config = {"from_attributes": True}


# Enhanced read schema with nested owner and inventory information
class TransactionReadDetailed(BaseModel):
	id: int
	title: str
	description: Optional[str]
	owner_id: int
	transaction_type: TransactionType
	amount_per_unit: Decimal
	quantity: Decimal
	purchase_price: Decimal
	total_amount: Decimal
	date: datetime
	inventory_id: Optional[int]
	owner: "UserReadSimple"
	inventory: Optional["InventoryReadSimple"] = None

	model_config = {"from_attributes": True}


# Import at the end to avoid circular imports
from app.schemas.user import UserReadSimple
from app.schemas.inventory import InventoryReadSimple

# Update forward references
TransactionReadDetailed.model_rebuild()
