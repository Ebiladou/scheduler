from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: int

class UserCreate(UserBase):
    password: str  

class UserResponse(UserBase):
    id: int  

    class Config:
        orm_mode = True 