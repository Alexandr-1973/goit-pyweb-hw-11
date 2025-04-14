from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas import ContactSchema, ContactResponseSchema

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/", response_model=list[ContactResponseSchema])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
        first_name: Optional[str] = Query(None),
        last_name: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    get_filters = {"first_name": first_name, "last_name": last_name, "email": email}
    use_get_filters={k:v for k,v in get_filters.items() if v}
    contacts = await repositories_contacts.get_contacts(limit, offset, use_get_filters, db)
    return contacts

@router.get("/birthday", response_model=list[ContactResponseSchema])
async def get_contacts(limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0), days: int = Query(7, ge=1), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_birthdays_contacts(limit, offset, days, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponseSchema)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact

