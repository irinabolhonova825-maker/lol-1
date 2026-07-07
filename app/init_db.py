from app.db.db import SessionLocal, engine
from app.db.models import Base, Category, Book
from app.db import crud

def init_db():
    # 1. Создаём таблицы
    print(" Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print(" Таблицы созданы успешно!")

    db = SessionLocal()
    try:
        # 2. Проверяем, есть ли уже категории
        if not crud.get_categories(db):
            print(" Добавление категорий...")
            
            # === ДОБАВЛЯЕМ ДВЕ КАТЕГОРИИ ===
            category1 = crud.create_category(db, "Художественная литература")
            category2 = crud.create_category(db, "Научная литература")
            
            print(f" Категория '{category1.title}' создана!")
            print(f" Категория '{category2.title}' создана!")

            # === ДОБАВЛЯЕМ КНИГИ К ПЕРВОЙ КАТЕГОРИИ (2-4 книги) ===
            books_category1 = [
                {"title": "Война и мир", "description": "Роман Льва Толстого", "price": 500.0, "category": category1.id},
                {"title": "Преступление и наказание", "description": "Роман Достоевского", "price": 450.0, "category": category1.id},
                {"title": "Мастер и Маргарита", "description": "Роман Булгакова", "price": 550.0, "category": category1.id},
            ]
            for book in books_category1:
                crud.create_book(db, **book)
            print(f" {len(books_category1)} книги добавлены в категорию '{category1.title}'")

            # === ДОБАВЛЯЕМ КНИГИ КО ВТОРОЙ КАТЕГОРИИ (2-4 книги) ===
            books_category2 = [
                {"title": "Краткая история времени", "description": "Стивен Хокинг о космосе", "price": 700.0, "category": category2.id},
                {"title": "Эволюция всего", "description": "Мэтт Ридли", "price": 600.0, "category": category2.id},
            ]
            for book in books_category2:
                crud.create_book(db, **book)
            print(f" {len(books_category2)} книги добавлены в категорию '{category2.title}'")
        else:
            print(" Данные уже существуют, пропускаем добавление.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()