from fastapi import status, HTTPException, APIRouter
from database import SessionDep
from models import Event
from schemas import EventCreate, EventResponse, EventUpdate
from sqlmodel import select

router = APIRouter(
    prefix="/event",
    tags=['Event']
)
