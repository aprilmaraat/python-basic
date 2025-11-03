from pydantic import BaseModel, field_validator
from typing import Optional, TYPE_CHECKING
from decimal import Decimal, ROUND_HALF_UP

if TYPE_CHECKING:
    from app.schemas.category import CategoryReadSimple
    from app.schemas.weight import WeightReadSimple

class InventoryBase(BaseModel):
    name: str
    shortname: Optional[str] = None
    purchase_price: Decimal
    selling_price: Decimal
    quantity: int
    category_id: int
    weight_id: int

    @field_validator("purchase_price", "selling_price", mode="before")
    def to_decimal(cls, v):  # type: ignore[override]
        if isinstance(v, (int, float, str)):
            return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return v

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    shortname: Optional[str] = None
    purchase_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    weight_id: Optional[int] = None

    @field_validator("purchase_price", "selling_price", mode="before")
    def to_decimal(cls, v):  # type: ignore[override]
        if v is None:
            return v
        if isinstance(v, (int, float, str)):
            return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return v

class InventoryRead(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    purchase_price: Decimal
    selling_price: Decimal
    quantity: int
    category_id: int
    weight_id: int
    model_config = {"from_attributes": True}

class InventoryReadSimple(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    purchase_price: Decimal
    selling_price: Decimal
    quantity: int
    category_id: int
    weight_id: int
    model_config = {"from_attributes": True}

# Enhanced read schema with nested category and weight information
class InventoryReadDetailed(BaseModel):
    id: int
    name: str
    shortname: Optional[str]
    purchase_price: Decimal
    selling_price: Decimal
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
