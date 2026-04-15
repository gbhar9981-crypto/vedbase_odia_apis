from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import List

from ..database_postgres import get_db
from .. import models, schemas

router = APIRouter(prefix="/contents", tags=["Verse Content"])

@router.post("/", response_model=schemas.VerseContentOut)
async def create_content(content: schemas.VerseContentCreate, db: AsyncSession = Depends(get_db)):
    new_content = models.VerseContent(**content.model_dump())
    db.add(new_content)
    await db.commit()
    await db.refresh(new_content)
    return new_content

@router.get("/{verse_id}", response_model=List[schemas.VerseContentOut])
async def get_contents_for_verse(verse_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.VerseContent).where(models.VerseContent.verse_id == verse_id))
    return result.scalars().all()

@router.put("/{id}", response_model=schemas.VerseContentOut)
async def update_content(id: int, content: schemas.VerseContentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(update(models.VerseContent).where(models.VerseContent.id == id).values(**content.model_dump()).returning(models.VerseContent))
    updated = result.scalars().first()
    if not updated:
        raise HTTPException(status_code=404, detail="Content not found")
    await db.commit()
    return updated

@router.delete("/{id}")
async def delete_content(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(models.VerseContent).where(models.VerseContent.id == id).returning(models.VerseContent.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Content not found")
    await db.commit()
    return {"message": "Content deleted successfully"}
