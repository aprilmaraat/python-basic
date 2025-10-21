from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.weight import Weight
from app.schemas.weight import WeightCreate, WeightUpdate


def get(db: Session, weight_id: int) -> Optional[Weight]:
    return db.get(Weight, weight_id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Weight]:
    stmt = select(Weight).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create(db: Session, obj_in: WeightCreate) -> Weight:
    db_obj = Weight(name=obj_in.name, description=obj_in.description)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Weight, obj_in: WeightUpdate) -> Weight:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Weight) -> Weight:
    db.delete(db_obj)
    db.commit()
    return db_obj