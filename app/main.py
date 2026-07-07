from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()
    try:
        print("\n" + "="*50)
        print(" СПИСОК КАТЕГОРИЙ И КНИГ")
        print("="*50)
        
        # Получаем все категории
        categories = crud.get_categories(db)
        
        if not categories:
            print(" Категории не найдены. Запустите init_db.py сначала.")
            return
        
        for cat in categories:
            print(f"\n КАТЕГОРИЯ: {cat.title} (ID: {cat.id})")
            print("-" * 40)
            
            # Получаем все книги
            all_books = crud.get_books(db)
            
            # Фильтруем книги по категории
            category_books = [book for book in all_books if book.category == cat.id]
            
            if category_books:
                for book in category_books:
                    print(f"     {book.title}")
                    print(f"     Описание: {book.description}")
                    print(f"     Цена: {book.price} руб.")
                    print()
            else:
                print("   В этой категории пока нет книг\n")
                
    finally:
        db.close()

if __name__ == "__main__":
    main()