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
        from_attributes = True 

class EventBase(BaseModel):
    title: str
    description: str | None = None
    event_date: str
    location: str
    image_url: str | None = None

class EventCreate(EventBase):
    category_id: int | None = None

class EventUpdate(EventBase):
    title: str | None = None
    event_date: str | None = None
    location: str | None = None

class EventResponse(EventBase):
    user_id: int
    id: int

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

class ContactCreate(ContactBase):
  phone: Optional[str] = None

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class LoginUser (BaseModel):
    email : str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    id: int | None = None