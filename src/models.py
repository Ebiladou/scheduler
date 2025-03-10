from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from typing import Optional, List

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str =  Field(sa_column=Column(String, unique=True, nullable=False))
    phone: Optional[str] = Field(sa_column=Column(String, unique=True, nullable=True))
    password: str
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.name}>"

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    def __repr__(self):
        return f"<Contact {self.name}>"

class EventCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))
    events: List["Event"] = Relationship(back_populates="category")

    def __repr__(self):
        return f"<EventCategory {self.name}>"
    

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str
    description: Optional[str] = None
    event_date: datetime = Field(sa_column=Column(DateTime, nullable=False))
    location: str
    image_url: Optional[str] = None
    category_id: Optional[int] = Field(foreign_key="eventcategory.id")
    category: Optional[EventCategory] = Relationship(back_populates="events")

    def __repr__(self):
        return f"<Event {self.title}>"

    
class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    event_id: int = Field(foreign_key="event.id")
    status: str = Field(default="pending") 
    sent_at: Optional[datetime] = None

    def __repr__(self):
        return f"<Notification {self.status} at {self.sent_at}>"
