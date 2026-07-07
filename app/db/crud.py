from sqlalchemy.orm import Session
from app.db import models

# ========== CRUD для категорий ==========

def create_category(db: Session, title: str):
    """Создать новую категорию"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Получить список категорий"""
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int):
    """Получить категорию по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def delete_category(db: Session, category_id: int):
    """Удалить категорию по ID"""
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# ========== CRUD для книг ==========

def create_book(db: Session, title: str, description: str, price: float, category: int, url: str = None):
    """Создать новую книгу"""
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category=category
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Получить список книг"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, **kwargs):
    """Обновить книгу"""
    db_book = get_book_by_id(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if hasattr(db_book, key):
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def delete_book(db: Session, book_id: int):
    """Удалить книгу по ID"""
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False