from fastapi import status, HTTPException, APIRouter, BackgroundTasks, Depends
from database import SessionDep
from models import Event, EventCategory, Notification
from schemas import EventCreate, EventResponse, EventUpdate
from sqlmodel import select
from oauth2 import verify_token
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/event",
    tags=['Event']
)

def schedule_notification(event: Event, session: SessionDep):
    notification_time = datetime.strptime(event.event_date, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=60)
    notification = Notification(
        user_id=event.user_id,
        event_id=event.id,
        status="pending",
        sent_at=notification_time.strftime("%Y-%m-%d %H:%M:%S")
    )
    session.add(notification)
    session.commit()

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, session: SessionDep, background_tasks: BackgroundTasks, logged_user=Depends(verify_token)):
    category = session.exec(select(EventCategory).where(EventCategory.id == event.category_id)).first()
    if not category and event.category_name:  
        session.add(category)
        session.commit()
        session.refresh(category)

    new_event = Event(**event.model_dump(exclude={"category_name"}), user_id=logged_user.id, category_id=category.id if category else None)
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    background_tasks.add_task(schedule_notification, new_event, session)
    return new_event

@router.get("/", response_model=list[EventResponse])
def get_event(session:SessionDep, logged_user = Depends(verify_token)):
    events = session.exec(select(Event)).all()
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
    return {"ok": True}

@router.patch("/{event_id}", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
def update_event (event_id:int, event:EventUpdate, session:SessionDep, logged_user = Depends(verify_token)):
    updated_event = session.get(Event, event_id)
    if not updated_event:
        raise HTTPException(status_code=404, detail="event not found")
    event_data = event.model_dump(exclude_unset=True)
    updated_event.sqlmodel_update(event_data)
    session.add(updated_event)
    session.commit()
    session.refresh(updated_event)
    return updated_event