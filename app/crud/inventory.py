from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate


def get(db: Session, inventory_id: int) -> Optional[Inventory]:
    return db.get(Inventory, inventory_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Inventory]:
    stmt = select(Inventory).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create(db: Session, obj_in: InventoryCreate) -> Inventory:
    db_obj = Inventory(
        name=obj_in.name,
        shortname=obj_in.shortname,
        quantity=obj_in.quantity,
        category_id=obj_in.category_id,
        weight_id=obj_in.weight_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Inventory, obj_in: InventoryUpdate) -> Inventory:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Inventory) -> Inventory:
    db.delete(db_obj)
    db.commit()
    return db_obj


def search(
    db: Session,
    *,
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    weight_id: Optional[int] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Inventory]:
    """Search inventory items with various filters."""
    filters = []
    
    if category_id is not None:
        filters.append(Inventory.category_id == category_id)
    
    if weight_id is not None:
        filters.append(Inventory.weight_id == weight_id)
    
    if min_quantity is not None:
        filters.append(Inventory.quantity >= min_quantity)
    
    if max_quantity is not None:
        filters.append(Inventory.quantity <= max_quantity)
    
    if q:
        like_exp = f"%{q.lower()}%"
        filters.append(
            or_(
                func.lower(Inventory.name).like(like_exp),
                func.lower(Inventory.shortname).like(like_exp),
            )
        )
    
    stmt = select(Inventory)
    if filters:
        stmt = stmt.where(and_(*filters))
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))