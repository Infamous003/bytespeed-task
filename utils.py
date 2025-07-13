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

def is_new_info(contacts, incomingEmail, incomingPhone):
    all_unique_emails = {c.email for c in contacts if c.email}
    all_unique_phones = {c.phoneNumber for c in contacts if c.phoneNumber}

    is_new_email = False
    is_new_phone = False

    if incomingEmail != "" and incomingEmail not in all_unique_emails:
        is_new_email = True
    if incomingPhone != "" and incomingPhone not in all_unique_phones:
        is_new_phone = True
    
    if is_new_email == True or is_new_phone == True:
        return True
    return False