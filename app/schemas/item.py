from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as dt_date
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
	title: str
	description: Optional[str] = None
	transaction_type: TransactionType = TransactionType.expense
	amount: int = 0
	date: dt_date = Field(default_factory=dt_date.today)


class TransactionCreate(TransactionBase):
	owner_id: int
	inventory_id: Optional[int] = None


class TransactionUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	transaction_type: Optional[TransactionType] = None
	amount: Optional[int] = None
	date: Optional[dt_date] = None
	inventory_id: Optional[int] = None


class TransactionRead(BaseModel):
	id: int
	title: str
	description: Optional[str]
	owner_id: int
	transaction_type: TransactionType
	amount: int
	date: dt_date
	inventory_id: Optional[int]

	model_config = {"from_attributes": True}


class TransactionReadSimple(BaseModel):
	id: int
	title: str
	transaction_type: TransactionType
	amount: int
	date: dt_date
	inventory_id: Optional[int]

	model_config = {"from_attributes": True}
