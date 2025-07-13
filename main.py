from fastapi import FastAPI, HTTPException, status, Depends
from database import create_db_and_tables, engine, get_session
from sqlmodel import Session, select, or_
from models import Contact, ContactCreate, LinkPrecedence, IdentificationModel
from utils import get_contacts_by_email_or_phone

app = FastAPI()

create_db_and_tables()

@app.get("/")
def root():
    return {"Hello": "World!"}

@app.post("/identify")
def identify_contact(contact: ContactCreate,
                     session: Session = Depends(get_session)):
    
    if not contact.email and not contact.phoneNumber:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Either email or phoneNumber must be provided")

    matchedContacts = get_contacts_by_email_or_phone(
        contact.email,
        contact.phoneNumber,
        session
    )
    # matchedContacts will contain all the contacts that match with either
    # the email or phone number

    # When no contacts matched either phone number or email
    # We create a complete NEW contact
    if not matchedContacts:
        new_contact = Contact(
            email=contact.email,
            phoneNumber=contact.phoneNumber,
            linkPrecedence=LinkPrecedence.primary
        )
        session.add(new_contact)
        session.commit()
        session.refresh(new_contact)
        
        contact_response = IdentificationModel(
            primaryContactId=new_contact.id,
            emails = [new_contact.email] if contact.email else [],
            phoneNumbers= [new_contact.phoneNumber] if contact.phoneNumber else [],
            secondaryContactIds= []
        )
        return {"contact" : contact_response}