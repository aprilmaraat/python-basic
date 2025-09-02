from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

def create_item(db: Session, item: ItemCreate, owner_id: int):
    db_item = Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def search_items(
    db: Session,
    *,
    owner_id: int | None = None,
    q: str | None = None,
    item_type: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    query = db.query(Item)

    if owner_id is not None:
        query = query.filter(Item.owner_id == owner_id)

    if item_type is not None:
        query = query.filter(Item.item_type == item_type)

    if q:
        ilike = f"%{q}%"
        query = query.filter(or_(Item.title.ilike(ilike), Item.description.ilike(ilike)))

    return query.offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
