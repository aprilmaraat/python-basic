from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import UserRead, UserCreate, UserUpdate, UserReadSimple

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserReadSimple, status_code=201)
def create_user(*, db: Session = Depends(get_db), obj_in: UserCreate):
	try:
		return crud_user.create(db, obj_in)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[UserReadSimple])
def list_users(
	*, db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)
):
	return crud_user.get_multi(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(*, db: Session = Depends(get_db), user_id: int):
	db_obj = crud_user.get(db, user_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="User not found")
	return db_obj


@router.put("/{user_id}", response_model=UserRead)
def update_user(*, db: Session = Depends(get_db), user_id: int, obj_in: UserUpdate):
	db_obj = crud_user.get(db, user_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="User not found")
	try:
		return crud_user.update(db, db_obj, obj_in)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", response_model=UserReadSimple)
def delete_user(*, db: Session = Depends(get_db), user_id: int):
	db_obj = crud_user.get(db, user_id)
	if not db_obj:
		raise HTTPException(status_code=404, detail="User not found")
	return crud_user.remove(db, db_obj)
