from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.item import Item, ItemCreate
from app.crud import item as crud_item

router = APIRouter()

@router.post("/{owner_id}", response_model=Item)
def create_item_for_user(owner_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return crud_item.create_item(db, item, owner_id)

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_item.get_items(db, skip=skip, limit=limit)
