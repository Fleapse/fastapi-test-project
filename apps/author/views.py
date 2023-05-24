from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from .schemas import AuthorBookSchema, AuthorSchema
from .models import Author
from main.db import get_session


router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[AuthorBookSchema])
async def get_authors(session: AsyncSession = Depends(get_session)):
    authors = await session.execute(select(Author).options(selectinload(Author.books)))
    return authors.scalars().all()

@router.get("/{author_id}", response_model=AuthorBookSchema)
async def get_author(author_id: int, session: AsyncSession = Depends(get_session)):
    author = await session.execute(select(Author).where(Author.id == author_id).options(selectinload(Author.books)))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404)
    return author

@router.post("/", response_model=AuthorSchema)
async def create_author(author: AuthorSchema, session: AsyncSession = Depends(get_session)):
    author = Author(**author.dict())
    session.add(author)
    await session.commit(), 
    return author

@router.post("/bulk_create", response_model=list[AuthorSchema])
async def create_authors(authors: list[AuthorSchema], session: AsyncSession = Depends(get_session)):
    authors = [Author(**author.dict()) for author in authors]
    session.add_all(authors)
    await session.commit(), 
    return authors
