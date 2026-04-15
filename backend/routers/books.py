from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List

from ..database_postgres import get_db
from .. import models, schemas

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=schemas.BookOut)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schemas.BookOut])
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).order_by(models.Book.id))
    return result.scalars().all()

@router.get("/{id}", response_model=schemas.BookOut)
async def get_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).where(models.Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{id}", response_model=schemas.BookOut)
async def update_book(id: int, book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(update(models.Book).where(models.Book.id == id).values(**book.model_dump()).returning(models.Book))
    updated_book = result.scalars().first()
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.commit()
    return updated_book

@router.delete("/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(models.Book).where(models.Book.id == id).returning(models.Book.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Book not found")
    await db.commit()
    return {"message": "Book deleted successfully"}
