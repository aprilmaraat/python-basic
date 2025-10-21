from pydantic import BaseModel
from typing import Optional

class WeightBase(BaseModel):
    name: str
    description: Optional[str] = None

class WeightCreate(WeightBase):
    pass

class WeightUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WeightRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    model_config = {"from_attributes": True}

class WeightReadSimple(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}
