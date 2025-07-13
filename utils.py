from sqlmodel import Session, select, or_
from models import Contact

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
