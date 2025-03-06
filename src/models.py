from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String
from datetime import datetime
from typing import Optional


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str =  Field(sa_column=Column(String, unique=True, nullable=False))
    phone: Optional[str] = Field(sa_column=Column(String, unique=True, nullable=True))
    password: str
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.name}>"

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    event_date: str
    location: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = Field(foreign_key="eventcategory.id")

    def __repr__(self):
        return f"<Event {self.title}>"

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    def __repr__(self):
        return f"<Contact {self.name}>"

class EventCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))

    def __repr__(self):
        return f"<EventCategory {self.name}>"

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")
    status: str
    sent_at: Optional[str] = None

    def __repr__(self):
        return f"<Notification {self.sent_at}>"