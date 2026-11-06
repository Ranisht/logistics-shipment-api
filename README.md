# Logistics Shipment Management API

A backend REST API built using FastAPI and PostgreSQL for managing shipments, tracking numbers, and shipment status history.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest

## Project Structure

```text
Logistics_shipment_api/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── alembic.ini
├── main.py
└── requirements.txt
```

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Logistics_shipment_api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and configure your local PostgreSQL database credentials.

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the application

```bash
uvicorn main:app --reload
```

## API Documentation

Once the application starts, visit:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Testing

```bash
pytest -v
```
