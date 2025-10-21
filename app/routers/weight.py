from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.crud import weight as crud_weight
from app.schemas.weight import WeightRead, WeightCreate, WeightUpdate, WeightReadSimple

router = APIRouter(prefix="/weights", tags=["weights"])

@router.post("", response_model=WeightReadSimple, status_code=201)
def create_weight(*, db: Session = Depends(get_db), obj_in: WeightCreate):
    return crud_weight.create(db, obj_in)

@router.get("", response_model=list[WeightReadSimple])
def list_weights(*, db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return crud_weight.get_multi(db, skip=skip, limit=limit)

@router.get("/{weight_id}", response_model=WeightRead)
def get_weight(*, db: Session = Depends(get_db), weight_id: int):
    db_obj = crud_weight.get(db, weight_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Weight not found")
    return db_obj

@router.put("/{weight_id}", response_model=WeightRead)
def update_weight(*, db: Session = Depends(get_db), weight_id: int, obj_in: WeightUpdate):
    db_obj = crud_weight.get(db, weight_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Weight not found")
    return crud_weight.update(db, db_obj, obj_in)

@router.delete("/{weight_id}", response_model=WeightReadSimple)
def delete_weight(*, db: Session = Depends(get_db), weight_id: int):
    db_obj = crud_weight.get(db, weight_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Weight not found")
    return crud_weight.remove(db, db_obj)