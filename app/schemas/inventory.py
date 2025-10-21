from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    name: str
    shortname: Optional[str] = None
    purchase_price: int
    selling_price: int
    quantity: int
    category_id: int
    weight_id: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    shortname: Optional[str] = None
    purchase_price: Optional[int] = None
    selling_price: Optional[int] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    weight_id: Optional[int] = None

class InventoryRead(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    purchase_price: int
    selling_price: int
    quantity: int
    category_id: int
    weight_id: int
    model_config = {"from_attributes": True}

class InventoryReadSimple(BaseModel):
    id: int
    name: str
    selling_price: int
    quantity: int
    model_config = {"from_attributes": True}
