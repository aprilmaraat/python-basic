from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get(db: Session, user_id: int) -> Optional[User]:
	return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> Optional[User]:
	stmt = select(User).where(User.email == email)
	return db.scalar(stmt)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
	stmt = select(User).offset(skip).limit(limit)
	return list(db.scalars(stmt))


def create(db: Session, obj_in: UserCreate) -> User:
	if get_by_email(db, obj_in.email):
		raise ValueError("Duplicate email")
	db_obj = User(
		email=obj_in.email,
		full_name=obj_in.full_name,
		is_active=obj_in.is_active,
	)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj


def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
	data = obj_in.model_dump(exclude_unset=True)
	if "email" in data and data["email"] != db_obj.email:
		if get_by_email(db, data["email"]):
			raise ValueError("Duplicate email")
	for field, value in data.items():
		setattr(db_obj, field, value)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	return db_obj


def remove(db: Session, db_obj: User) -> User:
	db.delete(db_obj)
	db.commit()
	return db_obj
