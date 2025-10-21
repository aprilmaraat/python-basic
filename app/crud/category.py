from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get(db: Session, category_id: int) -> Optional[Category]:
    return db.get(Category, category_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    stmt = select(Category).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create(db: Session, obj_in: CategoryCreate) -> Category:
    db_obj = Category(name=obj_in.name, description=obj_in.description)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Category) -> Category:
    db.delete(db_obj)
    db.commit()
    return db_obj