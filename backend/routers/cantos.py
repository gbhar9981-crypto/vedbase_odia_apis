from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List, Optional

from ..database_postgres import get_db
from .. import models, schemas

router = APIRouter(prefix="/cantos", tags=["Cantos"])

@router.post("/", response_model=schemas.CantoOut)
async def create_canto(canto: schemas.CantoCreate, db: AsyncSession = Depends(get_db)):
    # check if book exists
    book_result = await db.execute(select(models.Book).where(models.Book.id == canto.book_id))
    if not book_result.scalars().first():
        raise HTTPException(status_code=400, detail="Book does not exist")

    new_canto = models.Canto(**canto.model_dump())
    db.add(new_canto)
    await db.commit()
    await db.refresh(new_canto)
    return new_canto

@router.get("/", response_model=List[schemas.CantoOut])
async def get_cantos(book_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Canto).order_by(models.Canto.canto_number)
    if book_id is not None:
        query = query.where(models.Canto.book_id == book_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/{id}", response_model=schemas.CantoOut)
async def update_canto(id: int, canto: schemas.CantoCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(update(models.Canto).where(models.Canto.id == id).values(**canto.model_dump()).returning(models.Canto))
    updated = result.scalars().first()
    if not updated:
        raise HTTPException(status_code=404, detail="Canto not found")
    await db.commit()
    return updated

@router.delete("/{id}")
async def delete_canto(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(models.Canto).where(models.Canto.id == id).returning(models.Canto.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Canto not found")
    await db.commit()
    return {"message": "Canto deleted successfully"}
