from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate, CategoryReadSimple

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=CategoryReadSimple, status_code=201)
def create_category(*, db: Session = Depends(get_db), obj_in: CategoryCreate):
    return crud_category.create(db, obj_in)

@router.get("", response_model=list[CategoryReadSimple])
def list_categories(*, db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return crud_category.get_multi(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(*, db: Session = Depends(get_db), category_id: int):
    db_obj = crud_category.get(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_obj

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(*, db: Session = Depends(get_db), category_id: int, obj_in: CategoryUpdate):
    db_obj = crud_category.get(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_category.update(db, db_obj, obj_in)

@router.delete("/{category_id}", response_model=CategoryReadSimple)
def delete_category(*, db: Session = Depends(get_db), category_id: int):
    db_obj = crud_category.get(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_category.remove(db, db_obj)