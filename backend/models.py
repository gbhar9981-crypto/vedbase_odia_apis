from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database_postgres import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    cantos = relationship("Canto", back_populates="book", cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")


class Canto(Base):
    __tablename__ = "cantos"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    canto_number = Column(Integer)
    title = Column(String(255))
    description = Column(Text)

    book = relationship("Book", back_populates="cantos")
    chapters = relationship("Chapter", back_populates="canto", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"
    __table_args__ = (UniqueConstraint('book_id', 'chapter_number', name='unique_chapter'),)

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    canto_id = Column(Integer, ForeignKey("cantos.id", ondelete="CASCADE"), nullable=True)
    chapter_number = Column(Integer)
    title = Column(String(255))
    description = Column(Text)

    book = relationship("Book", back_populates="chapters")
    canto = relationship("Canto", back_populates="chapters")
    verses = relationship("Verse", back_populates="chapter", cascade="all, delete-orphan")


class Verse(Base):
    __tablename__ = "verses"
    __table_args__ = (UniqueConstraint('chapter_id', 'verse_number', name='unique_verse'),)

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"))
    verse_number = Column(Integer)

    chapter = relationship("Chapter", back_populates="verses")
    contents = relationship("VerseContent", back_populates="verse", cascade="all, delete-orphan")


class VerseContent(Base):
    __tablename__ = "verse_contents"
    id = Column(Integer, primary_key=True, index=True)
    verse_id = Column(Integer, ForeignKey("verses.id", ondelete="CASCADE"))
    sloka = Column(Text)
    synonyms = Column(Text)
    translation = Column(Text)
    purport = Column(Text)  # This will store JSON/HTML from flutter_quill
    language = Column(String(10), default='en')
    status = Column(String(20), default='draft')  # draft or published
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    verse = relationship("Verse", back_populates="contents")
