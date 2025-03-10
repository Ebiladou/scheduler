from fastapi import HTTPException, APIRouter, Depends
from datetime import timedelta
from sqlmodel import Session, select
from models import Notification, Event, Contact, Users
from database import SessionDep
from services.whatsappservice import send_whatsapp_message
from services.emailservice import send_email

router = APIRouter(
    prefix="/notification",
    tags=['Notification']
)

def schedule_notification(session: Session, event: Event):
    notification_time = event.event_date - timedelta(minutes=60)
    notification = Notification(user_id=event.user_id, event_id=event.id, status="scheduled", sent_at=notification_time)
    session.add(notification)
    session.commit()

def send_notification(session: Session, event: Event):
    notification = session.exec(select(Notification).where(Notification.event_id==event.id, Notification.status=="scheduled")).first()
    if notification:
        user = session.exec(select(Users).where(Users.id==event.user_id)).first()
        message = f"Reminder: Your event '{event.title}' is scheduled soon. Confirm or cancel."
        send_email(user.email, "Event Reminder", message)
        send_whatsapp_message(user.phone, message)
        notification.status = "Sent"
        session.commit()

def notify_contacts(session: Session, event: Event):
    contacts = session.exec(select(Contact).where(Contact.user_id==event.user_id)).all()
    user = session.exec(select(Users).where(Users.id==event.user_id)).first()
    message = f"{user.name} has confirmed attendance for '{event.title}'. Event details: {event.location} on {event.event_date}."
    for contact in contacts:
        if contact.email:
            send_email(contact.email, "Safety Alert", message)
        if contact.phone:
            send_whatsapp_message(contact.phone, message)

@router.post("/{event_id}/confirm")
def confirm_event(event_id: int, session: SessionDep):
    event = session.exec(select(Event).where(Event.id==event_id)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    notify_contacts(session, event)
    return {"message": "Event confirmed and contacts notified"}


@router.post("/{event_id}/cancel")
def cancel_event(event_id: int, session: SessionDep):
    event = session.exec(select(Event).where(Event.id==event_id)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    notification = session.exec(select(Notification).where(Notification.event_id==event_id)).first()
    if notification:
        notification.status = "Cancelled"
        session.commit()
    
    return {"message": "Event cancelled"}