from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.item import TransactionReadSimple


class UserBase(BaseModel):
	email: EmailStr
	full_name: Optional[str] = None
	is_active: bool = True


class UserCreate(UserBase):
	pass


class UserUpdate(BaseModel):
	email: Optional[EmailStr] = None
	full_name: Optional[str] = None
	is_active: Optional[bool] = None


class UserRead(BaseModel):
	id: int
	email: EmailStr
	full_name: Optional[str] = None
	is_active: bool
	transactions: List[TransactionReadSimple] = []

	model_config = {"from_attributes": True}


class UserReadSimple(BaseModel):
	id: int
	email: EmailStr
	full_name: Optional[str] = None
	is_active: bool

	model_config = {"from_attributes": True}
