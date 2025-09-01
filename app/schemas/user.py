from pydantic import BaseModel
from pydantic import ConfigDict

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)