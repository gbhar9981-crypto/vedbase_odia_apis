from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from ..database_postgres import get_db
from .. import models, schemas

router = APIRouter(prefix="/verses", tags=["Verses"])

@router.post("/", response_model=schemas.VerseOut)
async def create_verse(verse: schemas.VerseCreate, db: AsyncSession = Depends(get_db)):
    new_verse = models.Verse(**verse.model_dump())
    db.add(new_verse)
    try:
        await db.commit()
        await db.refresh(new_verse)
        return new_verse
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Verse with this number already exists for this chapter")

@router.get("/", response_model=List[schemas.VerseOut])
async def get_verses(chapter_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Verse).order_by(models.Verse.verse_number)
    if chapter_id is not None:
        query = query.where(models.Verse.chapter_id == chapter_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/{id}", response_model=schemas.VerseOut)
async def update_verse(id: int, verse: schemas.VerseCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(update(models.Verse).where(models.Verse.id == id).values(**verse.model_dump()).returning(models.Verse))
        updated = result.scalars().first()
        if not updated:
            raise HTTPException(status_code=404, detail="Verse not found")
        await db.commit()
        return updated
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Verse with this number already exists for this chapter")

@router.delete("/{id}")
async def delete_verse(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(models.Verse).where(models.Verse.id == id).returning(models.Verse.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Verse not found")
    await db.commit()
    return {"message": "Verse deleted successfully"}
