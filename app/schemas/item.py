from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Literal
from datetime import date as datetime_date
from typing import Optional

class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the item")
    description: str | None = Field(None, max_length=500, description="Optional description of the item")
    amount: int = Field(..., ge=0, description="Amount as an integer (e.g., 1000 for $10.00)")
    date: Optional[datetime_date] = Field(default=None, description="Date of the item (YYYY-MM-DD format)")
    item_type: Literal["expense", "earning"] = Field(..., description="Type of item: 'expense' or 'earning'")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Grocery Shopping",
                "description": "Weekly grocery shopping at the supermarket",
                "amount": 15000,
                "date": "2024-01-15",
                "item_type": "expense"
            }
        }
    )

class ItemCreate(ItemBase):
    owner_id: int = Field(..., description="ID of the user who owns this item")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Grocery Shopping",
                "description": "Weekly grocery shopping at the supermarket",
                "amount": 15000,
                "date": "2024-01-15",
                "item_type": "expense",
                "owner_id": 1
            }
        }
    )

class ItemUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100, description="Title of the item")
    description: str | None = Field(None, max_length=500, description="Optional description of the item")
    amount: int | None = Field(None, ge=0, description="Amount as an integer (e.g., 1000 for $10.00)")
    date: Optional[datetime_date] = Field(default=None, description="Date of the item (YYYY-MM-DD format)")
    item_type: Literal["expense", "earning"] | None = Field(None, description="Type of item: 'expense' or 'earning'")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Grocery Shopping",
                "amount": 12000
            }
        }
    )

class Item(ItemBase):
    id: int = Field(..., description="Unique identifier for the item")
    owner_id: int | None = Field(None, description="ID of the user who owns this item")

    model_config = ConfigDict(from_attributes=True)