from fastapi import status, HTTPException, APIRouter, Depends
from database import SessionDep
from models import Contact
from schemas import ContactCreate, ContactResponse, ContactUpdate
from sqlmodel import select
from oauth2 import verify_token

router = APIRouter(
    prefix="/contact",
    tags=['Contact']
)

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, session: SessionDep, logged_user = Depends(verify_token)):
    
    statement = select (Contact).where(((Contact.email == contact.email) | (Contact.phone == contact.phone)) & (Contact.user_id == logged_user.id))
    existing_contact = session.exec(statement).first()
    if existing_contact:
        raise HTTPException(status_code=403, detail="contact alredy exist")
    
    new_contact = Contact(**contact.model_dump(), user_id=logged_user.id)
    session.add(new_contact)
    session.commit()
    session.refresh(new_contact)
    return new_contact

@router.get("/", response_model=list[ContactResponse])
def get_contact(session:SessionDep, logged_user = Depends(verify_token)):
    contacts = session.exec(select(Contact)).all()
    return contacts 

@router.get("/{contact_id}", response_model=ContactResponse)
def getone_contact (contact_id:int, session: SessionDep, logged_user = Depends(verify_token)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact does not exist")
    return contact 

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id:int, session:SessionDep, logged_user = Depends(verify_token)):
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact not found")
    session.delete(contact)
    session.commit()
    return {"ok": True}

@router.patch("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_202_ACCEPTED)
def update_contact(contact_id:int, contact: ContactUpdate, session:SessionDep, logged_user = Depends(verify_token)):

    updated_contact = session.get(Contact, contact_id)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="contact not found")
    
    statement = select(Contact).where(((Contact.email == contact.email) | (Contact.phone == contact.phone)) & (Contact.user_id == logged_user.id) & (Contact.id != contact_id))
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=403, detail="email or phone already exist")
    
    contact_data = contact.model_dump(exclude_unset=True)
    updated_contact.sqlmodel_update(contact_data)
    session.add(updated_contact)
    session.commit()
    session.refresh(updated_contact)
    return updated_contact