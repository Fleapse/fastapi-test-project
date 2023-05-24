from main.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    author_id = Column(ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")