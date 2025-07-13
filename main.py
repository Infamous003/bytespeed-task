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
    
    # When there are matched contacts
    else:
        new_contact = None
        # Here, we find the oldest(primary) record
        # assuming the first contact to be 'primary'
        first_contact = matchedContacts[0]

        # If it's primary? cool, if not we get its linked primary contact.
        if first_contact.linkPrecedence == LinkPrecedence.primary:
            primary_contact = first_contact
        else:
            query = select(Contact).where(Contact.id == first_contact.linkedId)
            primary_contact = session.exec(query).first()

        # We collect all the unique emails and phone nums from the matched contacts list
        # Using Set() instead of List()
        all_unique_emails = {c.email for c in matchedContacts if c.email}
        all_unique_phones = {c.phoneNumber for c in matchedContacts if c.phoneNumber}

        is_email_nonempty = contact.email != ""
        is_phone_nonempty = contact.phoneNumber != ""

        # We need to find is th euser entered any new info, i.e, a new email or phoneNum
        # ONLY if the user provides some new info do we create a new Contact in DB
        is_new_email = False
        is_new_phone = False

        if is_email_nonempty and contact.email not in all_unique_emails:
            is_new_email = True
        if is_phone_nonempty and contact.phoneNumber not in all_unique_phones:
            is_new_phone = True
        
        should_create_new_model = False
        if is_new_email == True or is_new_phone == True:
            should_create_new_model = True

        if should_create_new_model:
            new_contact = Contact(
                email=contact.email if is_email_nonempty else None,
                phoneNumber=contact.phoneNumber if is_phone_nonempty else None,
                linkPrecedence=LinkPrecedence.secondary,
                linkedId=primary_contact.id
            )
            session.add(new_contact)
            session.commit()
            session.refresh(new_contact)

        linked_contacts = session.exec(
            select(Contact).where(
                or_(
                    Contact.id == primary_contact.id,
                    Contact.linkedId == primary_contact.id
                )
            )
        ).fetchall()
        emails = list({c.email for c in linked_contacts if c.email})
        phoneNumbers = list({c.phoneNumber for c in linked_contacts if c.phoneNumber})
        secondaryIds = [c.id for c in linked_contacts if c.linkPrecedence == LinkPrecedence.secondary]

        contact_response = IdentificationModel(
            primaryContactId=primary_contact.id,
            emails=emails,
            phoneNumbers=phoneNumbers,
            secondaryContactIds=secondaryIds
        )
        return {"contact": contact_response}
