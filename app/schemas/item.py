from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Literal

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    item_type: Literal["expense", "earning"]

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    item_type: Literal["expense", "earning"] | None = None

class Item(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)