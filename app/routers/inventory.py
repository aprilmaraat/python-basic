from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from app.db.session import get_db
from app.crud import inventory as crud_inventory
from app.crud import category as crud_category
from app.crud import weight as crud_weight
from app.schemas.inventory import InventoryRead, InventoryCreate, InventoryUpdate, InventoryReadSimple, InventoryReadDetailed

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/search", response_model=list[InventoryReadSimple])
def search_inventory(
    *,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None, description="Search in name or shortname"),
    category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
    weight_id: Optional[int] = Query(default=None, description="Filter by weight ID"),
    min_quantity: Optional[Decimal] = Query(default=None, ge=0, description="Minimum quantity"),
    max_quantity: Optional[Decimal] = Query(default=None, ge=0, description="Maximum quantity"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    """Search inventory items with various filters."""
    return crud_inventory.search(
        db,
        q=q,
        category_id=category_id,
        weight_id=weight_id,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        skip=skip,
        limit=limit,
    )

@router.post("", response_model=InventoryReadSimple, status_code=201)
def create_inventory(*, db: Session = Depends(get_db), obj_in: InventoryCreate):
    if not crud_category.get(db, obj_in.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    if not crud_weight.get(db, obj_in.weight_id):
        raise HTTPException(status_code=404, detail="Weight not found")
    return crud_inventory.create(db, obj_in)

@router.get("", response_model=list[InventoryReadSimple])
def list_inventory(*, db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return crud_inventory.get_multi(db, skip=skip, limit=limit)

@router.get("/{inventory_id}", response_model=InventoryRead)
def get_inventory(*, db: Session = Depends(get_db), inventory_id: int):
    db_obj = crud_inventory.get(db, inventory_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_obj

@router.get("/{inventory_id}/detailed", response_model=InventoryReadDetailed)
def get_inventory_detailed(*, db: Session = Depends(get_db), inventory_id: int):
    """Get inventory with detailed category and weight information."""
    db_obj = crud_inventory.get(db, inventory_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_obj

@router.put("/{inventory_id}", response_model=InventoryRead)
def update_inventory(*, db: Session = Depends(get_db), inventory_id: int, obj_in: InventoryUpdate):
    db_obj = crud_inventory.get(db, inventory_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inventory not found")
    # Validate category_id if being updated
    if obj_in.category_id is not None and obj_in.category_id != db_obj.category_id:
        if not crud_category.get(db, obj_in.category_id):
            raise HTTPException(status_code=404, detail="Category not found")
    # Validate weight_id if being updated
    if obj_in.weight_id is not None and obj_in.weight_id != db_obj.weight_id:
        if not crud_weight.get(db, obj_in.weight_id):
            raise HTTPException(status_code=404, detail="Weight not found")
    return crud_inventory.update(db, db_obj, obj_in)

@router.delete("/{inventory_id}", response_model=InventoryReadSimple)
def delete_inventory(*, db: Session = Depends(get_db), inventory_id: int):
    db_obj = crud_inventory.get(db, inventory_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return crud_inventory.remove(db, db_obj)