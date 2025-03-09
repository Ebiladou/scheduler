from database import SessionDep
from models import Event, Contact
from sqlmodel import select

def send_safety_contact_alert(event: Event, session: SessionDep):
    contacts = session.exec(
        select(Contact).where(Contact.user_id == event.user_id)
    ).all()

    if not contacts:
        return
    
    message = f"Your contact {event.user_id} has confirmed their attendance for {event.title}.\n" \
              f"Location: {event.location}\n Date: {event.event_date}\n"

    for contact in contacts:
        if contact.contact_method == "email":
            send_email(contact.contact_info, "Event Confirmation", message)
        elif contact.contact_method == "whatsapp":
            send_whatsapp(contact.contact_info, message)


def send_email(to_email, subject, message):
    print(f"Sending email to {to_email}: {subject} - {message}")


def send_whatsapp(to_number, message):
    print(f"Sending WhatsApp to {to_number}: {message}")
