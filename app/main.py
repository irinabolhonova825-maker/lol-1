from fastapi import FastAPI
from app.api import books, categories

# Создаём экземпляр приложения FastAPI
app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

# Подключаем роутеры из модулей books и categories
app.include_router(books.router)
app.include_router(categories.router)


# Эндпоинт для проверки, что сервис жив
@app.get("/health")
def health_check():
    """
    Проверка работоспособности сервиса.
    """
    return {"status": "OK", "message": "Service is running"}