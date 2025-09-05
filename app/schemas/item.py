from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Literal
from datetime import date
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    amount: int
    date: Optional[date] = None
    item_type: Literal["expense", "earning"]

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    amount: int | None = None
    date: Optional[date] = None
    item_type: Literal["expense", "earning"] | None = None

class Item(ItemBase):
    id: int
    owner_id: int | None = None

    model_config = ConfigDict(from_attributes=True)