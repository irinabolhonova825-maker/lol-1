API для управления книгами и категориями на FastAPI + PostgreSQL.

ЗАПУСК ПРОЕКТА:
1. Активируйте виртуальное окружение:
source venv/bin/activate

2. Установите зависимости:
pip install -r requirements.txt

3. Запустите сервер:
uvicorn app.main:app --reload

4. Откройте в браузере:
Swagger-документация: http://127.0.0.1:8000/docs
Проверка работы: http://127.0.0.1:8000/health

Скриншоты работы API находятся в папке examples/.