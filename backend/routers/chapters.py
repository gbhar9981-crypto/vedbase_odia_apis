from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from ..database_postgres import get_db
from .. import models, schemas

router = APIRouter(prefix="/chapters", tags=["Chapters"])

@router.post("/", response_model=schemas.ChapterOut)
async def create_chapter(chapter: schemas.ChapterCreate, db: AsyncSession = Depends(get_db)):
    new_chapter = models.Chapter(**chapter.model_dump())
    db.add(new_chapter)
    try:
        await db.commit()
        await db.refresh(new_chapter)
        return new_chapter
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Chapter with this number already exists for this book")

@router.get("/", response_model=List[schemas.ChapterOut])
async def get_chapters(book_id: Optional[int] = None, canto_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Chapter).order_by(models.Chapter.chapter_number)
    if book_id is not None:
        query = query.where(models.Chapter.book_id == book_id)
    if canto_id is not None:
        query = query.where(models.Chapter.canto_id == canto_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/{id}", response_model=schemas.ChapterOut)
async def update_chapter(id: int, chapter: schemas.ChapterCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(update(models.Chapter).where(models.Chapter.id == id).values(**chapter.model_dump()).returning(models.Chapter))
        updated = result.scalars().first()
        if not updated:
            raise HTTPException(status_code=404, detail="Chapter not found")
        await db.commit()
        return updated
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Chapter with this number already exists for this book")


@router.delete("/{id}")
async def delete_chapter(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(models.Chapter).where(models.Chapter.id == id).returning(models.Chapter.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Chapter not found")
    await db.commit()
    return {"message": "Chapter deleted successfully"}
