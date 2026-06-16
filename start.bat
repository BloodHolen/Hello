@echo off
chcp 65001 >nul
if not exist .env (
    echo SECRET_KEY=django-insecure-default-key-change-me> .env
    echo DEBUG=True>> .env
)
call .venv\Scripts\activate.bat
python manage.py runserver
pause
