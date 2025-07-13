from sqlmodel import Session, select, or_
from models import Contact, LinkPrecedence

def get_contacts_by_email_or_phone(email: str,
                                   phoneNumber: str,
                                   session: Session):
    query = select(Contact).where(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phoneNumber
        )
    )

    contacts = session.exec(query).fetchall()

    return contacts

def get_primary_contact(contacts: list, session: Session):
    # assuming the first contact to be 'primary'
    first_contact = contacts[0]

    # If it's primary? cool, if not we get its linked primary contact
    if first_contact.linkPrecedence == LinkPrecedence.primary:
        primary_contact = first_contact
    else:
        query = select(Contact).where(Contact.id == first_contact.linkedId)
        primary_contact = session.exec(query).first()
    return primary_contact