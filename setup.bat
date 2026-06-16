@echo off
chcp 65001 >nul

:: Создать .venv если нет
if not exist .venv\Scripts\python.exe (
    echo [1/4] Создание виртуального окружения...
    python -m venv .venv
)

:: Активировать
call .venv\Scripts\activate.bat

:: Установить зависимости
echo [2/4] Установка зависимостей...
pip install -r requirements.txt

:: Создать .env если нет
if not exist .env (
    echo [3/4] Создание .env...
    (
        echo SECRET_KEY=django-insecure-default-key-change-me
        echo DEBUG=True
    ) > .env
)

:: Миграции
echo [4/4] Применение миграций...
python manage.py migrate

echo.
echo ========================================
echo Все готово! Используйте start.bat для запуска
echo ========================================
pause
