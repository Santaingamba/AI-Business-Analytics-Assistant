# Backend API

This is the FastAPI backend for the AI Business Analytics Assistant.

## Architecture

- **Presentation Layer**: `app/api`
- **Service Layer**: `app/services` (Business logic)
- **Repository Layer**: `app/db/repository.py`
- **Database Layer**: `app/db`

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```
