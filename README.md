# EduPath

Django-based study resources and career guidance MVP.

## Windows 11 Setup

1. Install Python 3.11+ and MySQL Server.
2. Create database:

   CREATE DATABASE edupath_db CHARACTER SET utf8mb4;

3. Copy `.env.example` to `.env`.
4. Set your MySQL password in `.env`.
5. Open terminal in the EduPath folder.

Run:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed_demo
    python manage.py createsuperuser
    python manage.py runserver

Website: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

The current recommendation engine is rule-based.
OCR currently supports images when Tesseract is installed.
PDF OCR and external certificate verification need additional integration.

Before deployment, configure HTTPS, secure SECRET_KEY,
DEBUG=False, ALLOWED_HOSTS and secure uploaded-file handling.
