from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from decimal import Decimal
from app.models.transaction import Transaction, TransactionType
from app.schemas.item import TransactionCreate, TransactionUpdate


def get(db: Session, transaction_id: int) -> Optional[Transaction]:
	return db.get(Transaction, transaction_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
	stmt = select(Transaction).offset(skip).limit(limit)
	return list(db.scalars(stmt))


def create(db: Session, obj_in: TransactionCreate) -> Transaction:
	db_obj = Transaction(
		title=obj_in.title,
		description=obj_in.description,
		owner_id=obj_in.owner_id,
		transaction_type=obj_in.transaction_type,
		amount_per_unit=Decimal(obj_in.amount_per_unit),
		quantity=Decimal(obj_in.quantity),
		purchase_price=Decimal(obj_in.purchase_price),
		date=obj_in.date,
		inventory_id=obj_in.inventory_id,
	)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj


def update(db: Session, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
	data = obj_in.model_dump(exclude_unset=True)
	for field, value in data.items():
		if field in ("amount_per_unit", "purchase_price", "quantity") and value is not None:
			value = Decimal(value)
		setattr(db_obj, field, value)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj


def remove(db: Session, db_obj: Transaction) -> Transaction:
	db.delete(db_obj)
	db.commit()
	return db_obj


def search(
	db: Session,
	*,
	owner_id: Optional[int] = None,
	q: Optional[str] = None,
	transaction_type: Optional[TransactionType] = None,
	date_from: Optional[datetime] = None,
	date_to: Optional[datetime] = None,
	inventory_id: Optional[int] = None,
	skip: int = 0,
	limit: int = 100,

) -> List[Transaction]:
	filters = []
	if owner_id is not None:
		filters.append(Transaction.owner_id == owner_id)
	if transaction_type is not None:
		filters.append(Transaction.transaction_type == transaction_type)
	if date_from is not None:
		filters.append(Transaction.date >= date_from)
	if date_to is not None:
		filters.append(Transaction.date <= date_to)
	if inventory_id is not None:
		filters.append(Transaction.inventory_id == inventory_id)
	if q:
		like_exp = f"%{q.lower()}%"
		filters.append(
			or_(
				func.lower(Transaction.title).like(like_exp),
				func.lower(Transaction.description).like(like_exp),
			)
		)
	stmt = select(Transaction)
	if filters:
		stmt = stmt.where(and_(*filters))
	stmt = stmt.offset(skip).limit(limit)
	return list(db.scalars(stmt))
