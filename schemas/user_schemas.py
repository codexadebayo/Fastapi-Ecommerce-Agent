from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    name: str



class UserRead(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    email: str
    name: str
    is_active: bool


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    # created_at: datetime
    # updated_at: datetime


