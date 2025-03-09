from fastapi import status, HTTPException, APIRouter, Depends
from database import SessionDep
from models import Notification, Event
from sqlmodel import select
from oauth2 import verify_token
from message import send_safety_contact_alert

router = APIRouter(
    prefix="/notification",
    tags=['Notification']
)

@router.patch("/confirm/{event_id}", status_code=status.HTTP_200_OK)
def confirm_event(event_id: int, session: SessionDep, logged_user=Depends(verify_token)):
    event = session.get(Event, event_id)
    if not event or event.user_id != logged_user.id:
        raise HTTPException(status_code=404, detail="Event not found or unauthorized")

    notification = session.exec(
        select(Notification).where(Notification.event_id == event_id, Notification.user_id == logged_user.id)
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.status = "confirmed"
    session.add(notification)
    session.commit()
    send_safety_contact_alert(event, session) 
    return {"message": "Event confirmed. Safety contacts notified."}


@router.patch("/cancel/{event_id}", status_code=status.HTTP_200_OK)
def cancel_event(event_id: int, session: SessionDep, logged_user=Depends(verify_token)):
    event = session.get(Event, event_id)
    if not event or event.user_id != logged_user.id:
        raise HTTPException(status_code=404, detail="Event not found or unauthorized")

    notification = session.exec(
        select(Notification).where(Notification.event_id == event_id, Notification.user_id == logged_user.id)
    ).first()

    if notification:
        notification.status = "cancelled"
        session.add(notification)
        session.commit()

    return {"message": "Event cancelled. No notifications will be sent."}