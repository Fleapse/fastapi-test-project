from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func

from apps.author.models import Author
from apps.author.schemas import AuthorSchema

from .schemas import BookAuthorSchema, BookSchema

from .models import Book
from main.db import get_session


router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[BookAuthorSchema])
async def get_books(session: AsyncSession = Depends(get_session)):
    authors = await session.execute(select(Book).options(selectinload(Book.author)))
    return authors.scalars().all()

@router.get("/{book_id}", response_model=BookAuthorSchema)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await session.execute(select(Book).where(Book.id == book_id).options(selectinload(Book.author)))
    book = book.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404)
    return book

@router.post("/", response_model=BookAuthorSchema)
async def create_author(book: BookSchema, session: AsyncSession = Depends(get_session)):
    author = await session.execute(select(Author).where(Author.id == book.author_id))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404)
    book = Book(**book.dict())
    session.add(book)
    await session.commit()
    return BookAuthorSchema.from_orm(book)

@router.post("/bulk_create", response_model=list[BookAuthorSchema])
async def create_authors(books: list[BookSchema], session: AsyncSession = Depends(get_session)):
    author_ids = {book.author_id for book in books}
    author = await session.execute(select(Author).where(Author.id.in_(author_ids)))
    authors = author.scalars().all()
    if len(author_ids) != len(authors):
        raise HTTPException(status_code=404, detail="Один из авторов не существует")
    books = [Book(**book.dict()) for book in books]
    session.add_all(books)
    await session.commit()
    return [BookAuthorSchema.from_orm(book) for book in books]
