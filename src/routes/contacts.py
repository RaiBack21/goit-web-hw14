from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.schemas import ContactResponse, ContactModel
from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as rep_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more than 5 request per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def get_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await rep_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get(
    "/search",
    response_model=List[ContactResponse],
    description="No more than 10 request per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def search_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await rep_contacts.search_contacts(
        first_name, last_name, email, current_user, db
    )
    return contacts


@router.get(
    "/upcoming_birthdays",
    response_model=List[ContactResponse],
    description="No more than 5 request per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await rep_contacts.get_upcoming_birthdays(current_user, db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 10 request per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await rep_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    description="No more than 2 request per 5 minutes",
    dependencies=[Depends(RateLimiter(times=2, seconds=180))],
)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await rep_contacts.create_contact(body, current_user, db)


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 5 request per 2 minutes",
    dependencies=[Depends(RateLimiter(times=5, seconds=120))],
)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await rep_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 5 request per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def remove_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contact = await rep_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
