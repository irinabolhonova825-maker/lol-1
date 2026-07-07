from pydantic import BaseModel
from typing import Optional

# ===== СХЕМЫ ДЛЯ КАТЕГОРИЙ =====

class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# ===== СХЕМЫ ДЛЯ КНИГ =====

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category: int  # ID категории

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category: Optional[int] = None

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True