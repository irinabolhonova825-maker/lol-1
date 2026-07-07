# Импортируем необходимые модули из FastAPI и SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Импортируем наши модули
from app.db.db import get_db
from app.db import crud
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

# Создаём роутер с префиксом /categories и тегом "Categories" для Swagger
router = APIRouter(prefix="/categories", tags=["Categories"])


# 1. GET /categories — получить ВСЕ категории
@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    skip: int = 0,           # Сколько записей пропустить (для пагинации)
    limit: int = 100,        # Сколько записей показать
    db: Session = Depends(get_db)  # Получаем сессию БД
):
    """
    Возвращает список всех категорий.
    Можно указать skip и limit для постраничного вывода.
    """
    return crud.get_categories(db, skip=skip, limit=limit)


# 2. GET /categories/{id} — получить ОДНУ категорию по ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Возвращает категорию по её ID.
    Если категория не найдена — возвращает ошибку 404.
    """
    # Ищем категорию в БД
    db_category = crud.get_category_by_id(db, category_id)
    
    # Если не нашли — выбрасываем ошибку 404
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Если нашли — возвращаем её
    return db_category


# 3. POST /categories — СОЗДАТЬ новую категорию
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую категорию.
    Ожидает JSON с полем title.
    Возвращает созданную категорию с присвоенным ID.
    """
    return crud.create_category(db, title=category.title)


# 4. PUT /categories/{id} — ОБНОВИТЬ категорию
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: Session = Depends(get_db)
):
    """
    Обновляет название категории по её ID.
    Ожидает JSON с полем title.
    Если категория не найдена — возвращает ошибку 404.
    """
    # Вызываем функцию update_category из CRUD
    db_category = crud.update_category(db, category_id, title=category.title)
    
    # Если категория не найдена — ошибка 404
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return db_category


# 5. DELETE /categories/{id} — УДАЛИТЬ категорию
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Удаляет категорию по её ID.
    При успешном удалении возвращает статус 204 (No Content).
    Если категория не найдена — возвращает ошибку 404.
    """
    success = crud.delete_category(db, category_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # При статусе 204 тело ответа пустое, поэтому ничего не возвращаем
    return None