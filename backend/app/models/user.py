from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    name: str
    email: str
    age: int
    gender: int # 0 for male, 1 for female, 2 for other

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    gender: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = None