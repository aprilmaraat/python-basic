from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date as dt_date
from typing import Optional
from app.db.session import get_db
from app.crud import item as crud_transaction
from app.crud import user as crud_user
from app.schemas.item import (
	TransactionRead,
	TransactionCreate,
	TransactionUpdate,
	TransactionReadSimple,
	TransactionReadDetailed,
)
from app.models.transaction import TransactionType
from app.crud import inventory as crud_inventory

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/search", response_model=list[TransactionReadSimple])
def search_transactions(
	*,
	db: Session = Depends(get_db),
	owner_id: Optional[int] = Query(default=None),
	q: Optional[str] = Query(default=None),
	transaction_type: Optional[TransactionType] = Query(default=None),
	date_from: Optional[dt_date] = Query(default=None),
	date_to: Optional[dt_date] = Query(default=None),
	skip: int = Query(0, ge=0),
	limit: int = Query(100, ge=1),
):
	return crud_transaction.search(
		db,
		owner_id=owner_id,
		q=q,
		transaction_type=transaction_type,
		date_from=date_from,
		date_to=date_to,
		skip=skip,
		limit=limit,
	)


@router.post("", response_model=TransactionReadSimple, status_code=201)
def create_transaction(*, db: Session = Depends(get_db), obj_in: TransactionCreate):
	if not crud_user.get(db, obj_in.owner_id):
		raise HTTPException(status_code=404, detail="Owner not found")
	if obj_in.inventory_id is not None and not crud_inventory.get(db, obj_in.inventory_id):
		raise HTTPException(status_code=404, detail="Inventory not found")
	return crud_transaction.create(db, obj_in)


@router.get("", response_model=list[TransactionReadSimple])
def list_transactions(
	*, db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)
):
	return crud_transaction.get_multi(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(*, db: Session = Depends(get_db), transaction_id: int):
	db_obj = crud_transaction.get(db, transaction_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="Transaction not found")
	return db_obj


@router.get("/{transaction_id}/detailed", response_model=TransactionReadDetailed)
def get_transaction_detailed(*, db: Session = Depends(get_db), transaction_id: int):
	"""Get transaction with detailed owner and inventory information."""
	db_obj = crud_transaction.get(db, transaction_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="Transaction not found")
	return db_obj


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(*, db: Session = Depends(get_db), transaction_id: int, obj_in: TransactionUpdate):
	db_obj = crud_transaction.get(db, transaction_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="Transaction not found")
	if obj_in.inventory_id is not None and obj_in.inventory_id != db_obj.inventory_id:
		if obj_in.inventory_id is not None and not crud_inventory.get(db, obj_in.inventory_id):
			raise HTTPException(status_code=404, detail="Inventory not found")
	return crud_transaction.update(db, db_obj, obj_in)


@router.delete("/{transaction_id}", response_model=TransactionReadSimple)
def delete_transaction(*, db: Session = Depends(get_db), transaction_id: int):
	db_obj = crud_transaction.get(db, transaction_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="Transaction not found")
	return crud_transaction.remove(db, db_obj)
