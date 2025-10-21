from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
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
		amount=obj_in.amount,
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
	date_from: Optional[date] = None,
	date_to: Optional[date] = None,
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
