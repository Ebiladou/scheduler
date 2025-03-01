from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: int

class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    phone: int | None = None

class UserCreate(UserBase):
    password: str  

class UserResponse(UserBase):
    id: int  

    class Config:
        orm_mode = True 