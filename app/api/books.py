# Импорты
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

# Создаём роутер
router = APIRouter(prefix="/books", tags=["Books"])


# 1. GET /books — получить ВСЕ книги с фильтрацией по категории
@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    db: Session = Depends(get_db)
):
    """
    Возвращает список книг.
    Можно отфильтровать по категории: ?category_id=1
    """
    # Получаем все книги
    all_books = crud.get_books(db, skip=skip, limit=limit)
    
    # Если указан category_id — фильтруем
    if category_id:
        return [book for book in all_books if book.category == category_id]
    
    return all_books


# 2. GET /books/{id} — получить ОДНУ книгу по ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Возвращает книгу по её ID.
    Если книга не найдена — ошибка 404.
    """
    db_book = crud.get_book_by_id(db, book_id)
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book


# 3. POST /books — СОЗДАТЬ новую книгу
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую книгу.
    Ожидает JSON: title, description, price, category.
    Проверяет, что указанная категория существует.
    """
    # Проверяем, существует ли категория с таким ID
    category = crud.get_category_by_id(db, book.category)
    if category is None:
        # Если категории нет — ошибка 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Category does not exist")
    
    # Если категория есть — создаём книгу
    return crud.create_book(db, **book.dict())


# 4. PUT /books/{id} — ОБНОВИТЬ книгу
@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, 
    book: BookUpdate, 
    db: Session = Depends(get_db)
):
    """
    Обновляет книгу по ID.
    Можно обновить только часть полей.
    Если указана категория — проверяет её существование.
    """
    # Если в запросе указана категория — проверяем её
    if book.category is not None:
        category = crud.get_category_by_id(db, book.category)
        if category is None:
            raise HTTPException(status_code=400, detail="Category does not exist")
    
    # Обновляем книгу (exclude_unset=True — обновляем только переданные поля)
    db_book = crud.update_book(db, book_id, **book.dict(exclude_unset=True))
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book


# 5. DELETE /books/{id} — УДАЛИТЬ книгу
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Удаляет книгу по ID.
    """
    success = crud.delete_book(db, book_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return None