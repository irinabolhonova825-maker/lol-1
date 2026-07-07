from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)

    # Связь с книгами (один ко многим)
    books = relationship("Book", back_populates="category_rel")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String(500), nullable=True)
    
    # Внешний ключ на таблицу categories
    category = Column(Integer, ForeignKey("categories.id"))

    # Связь с категорией
    category_rel = relationship("Category", back_populates="books")