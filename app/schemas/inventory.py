from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.category import CategoryReadSimple
    from app.schemas.weight import WeightReadSimple

class InventoryBase(BaseModel):
    name: str
    shortname: Optional[str] = None
    quantity: int
    category_id: int
    weight_id: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    shortname: Optional[str] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    weight_id: Optional[int] = None

class InventoryRead(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    quantity: int
    category_id: int
    weight_id: int
    model_config = {"from_attributes": True}

class InventoryReadSimple(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    quantity: int
    category_id: int
    weight_id: int
    model_config = {"from_attributes": True}

# Enhanced read schema with nested category and weight information
class InventoryReadDetailed(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    quantity: int
    category_id: int
    weight_id: int
    category: "CategoryReadSimple"
    weight: "WeightReadSimple"
    model_config = {"from_attributes": True}

# Import at the end to avoid circular imports
from app.schemas.category import CategoryReadSimple
from app.schemas.weight import WeightReadSimple

# Update forward references
InventoryReadDetailed.model_rebuild()
