from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db.session import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.crud import item as crud_item

router = APIRouter()

@router.post("/", response_model=Item, summary="Create a new item", description="Create a new expense or earning item for a user")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    
    - **title**: Title of the item (required, 1-100 characters)
    - **description**: Optional description (max 500 characters)
    - **amount**: Amount as integer (required, >= 0, e.g., 1000 for $10.00)
    - **date**: Date in YYYY-MM-DD format (optional, defaults to today)
    - **item_type**: Either "expense" or "earning" (required)
    - **owner_id**: ID of the user who owns this item (required)
    """
    return crud_item.create_item(db, item)

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_item.get_items(db, skip=skip, limit=limit)

# Search items with optional filters
@router.get("/search", response_model=List[Item])
def search_items(
    owner_id: int | None = None,
    q: str | None = None,
    item_type: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return crud_item.search_items(
        db,
        owner_id=owner_id,
        q=q,
        item_type=item_type,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_item.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud_item.update_item(db, item_id=item_id, item_update=item_update)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", response_model=Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_item.delete_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
