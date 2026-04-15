from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CantoBase(BaseModel):
    canto_number: int
    title: Optional[str] = None
    description: Optional[str] = None

class CantoCreate(CantoBase):
    book_id: int

class CantoOut(CantoBase):
    id: int
    book_id: int
    model_config = ConfigDict(from_attributes=True)

class ChapterBase(BaseModel):
    chapter_number: int
    title: Optional[str] = None
    description: Optional[str] = None

class ChapterCreate(ChapterBase):
    book_id: int
    canto_id: Optional[int] = None

class ChapterOut(ChapterBase):
    id: int
    book_id: int
    canto_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class VerseBase(BaseModel):
    verse_number: int

class VerseCreate(VerseBase):
    chapter_id: int

class VerseOut(VerseBase):
    id: int
    chapter_id: int
    model_config = ConfigDict(from_attributes=True)

class VerseContentBase(BaseModel):
    sloka: Optional[str] = None
    synonyms: Optional[str] = None
    translation: Optional[str] = None
    purport: Optional[str] = None
    language: Optional[str] = "en"
    status: Optional[str] = "draft"

class VerseContentCreate(VerseContentBase):
    verse_id: int

class VerseContentOut(VerseContentBase):
    id: int
    verse_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
