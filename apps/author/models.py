from main.db import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")