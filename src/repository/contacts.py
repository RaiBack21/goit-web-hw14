from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return (
        db.query(Contact).filter(Contact.user == user).offset(skip).limit(limit).all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    return contact


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_info=body.additional_info,
        user=user,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(
    body: ContactModel, contact_id: int, user: User, db: Session
) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the nocontactte to update.
    :type contact_id: int
    :param body: The updated data for the ncontactote.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(
    first_name: Optional[str], last_name: Optional[str], email: Optional[str], user: User, db: Session
) -> List[Contact]:
    """
    Searches for contacts by first name, last name and email for a specific user.

    :param first_name: First name to search for a contacts.
    :type first_name: str
    :param last_name: Last name to search for a contacts.
    :type last_name: str
    :param email: Email to search for a contacts.
    :type email: str
    :param user: The user to search the contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of found contacts.
    :rtype: List[Contact]
    """
    
    contacts = db.query(Contact).filter(Contact.user == user)
    if first_name:
        contacts = contacts.filter(Contact.first_name == first_name)

    if last_name:
        contacts = contacts.filter(Contact.last_name == last_name)

    if email:
        contacts = contacts.filter(Contact.email == email)

    return contacts.all()


async def get_upcoming_birthdays(user: User, db: Session) -> List[Contact]:
    """
    Searches for contacts whose birthdays is in the next 7 days.

    :param user: The user to search the contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The list of found contacts.
    :rtype: List[Contact]
    """
    today = datetime.today()
    contacts = db.query(Contact).filter(Contact.user == user).all()
    result = []

    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)
        if today.date() <= birthday <= (today + timedelta(days=7)).date():
            result.append(contact)

    return result
