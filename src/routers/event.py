from fastapi import status, HTTPException, APIRouter, Depends
from database import SessionDep
from models import Event
from schemas import EventCreate, EventResponse, EventUpdate
from sqlmodel import select
from oauth2 import verify_token

router = APIRouter(
    prefix="/event",
    tags=['Event']
)

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event:EventCreate, session:SessionDep, logged_user = Depends(verify_token)):
    if event.user_id != logged_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create an event for this user")
    new_event = Event(**event.model_dump())
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

@router.get("/", response_model=EventResponse)
def get_event(session:SessionDep, logged_user = Depends(verify_token)):
    events = session.exec(select(Event)).all
    return events

@router.get("/{event_id}", response_model=EventResponse)
def getone_event (event_id: int, session: SessionDep, logged_user=Depends(verify_token)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException (status_code=404, detail="event not found")
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id:int, session:SessionDep, logged_user=Depends(verify_token)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    session.delete(event)
    session.commit()
    return ("ok:" True)

@router.patch("/{event_id}", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
def update_event (event_id:int, event:EventUpdate, session:SessionDep, logged_user = Depends(verify_token)):
    updated_event = session.get(Event, event_id)
    if not updated_event:
        raise HTTPException(status_code=404, detail="event not found")
    event_data = event.model_dump(exclude_unset=True)
    updated_event.sqlmodel_update(event_data)
    session.add(updated_event)
    session.commit
    session.refresh(updated_event)
    return updated_event