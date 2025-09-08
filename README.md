FastAPI with SQLAlchemy (CRUD Example)

This project is a simple CRUD API built with FastAPI, SQLAlchemy, and Pydantic. It provides endpoints for managing Users and Items, with an SQLite database for persistence.

🚀 Features

User management (create, read, update, delete)

Item management (create, read, update, delete)

SQLite database integration

Interactive API documentation (/docs and /redoc)

Modular and extensible structure

📦 Requirements

Python 3.9+

Dependencies listed in requirements.txt:

fastapi

uvicorn

sqlalchemy

pydantic

pydantic-settings

⚙️ Setup

1. Clone Repository
git clone <your-repo-url>
cd python-basic

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Application
python -m uvicorn main:app --reload


The app will be available at:
👉 http://127.0.0.1:8000

Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

📂 Project Structure

python-basic/
│── main.py                # Entry point
│── requirements.txt       # Dependencies
│── fastapi.db             # SQLite database
│── app/
│   ├── routers/
│   │   ├── user.py        # User routes
│   │   ├── item.py        # Item routes
│   ├── schemas/           # Pydantic models
│   ├── crud/              # CRUD functions
│   ├── db/
│   │   └── session.py     # DB session and engine
│   ├── models/            # SQLAlchemy models
│   │   ├── user.py
│   │   └── item.py
│   └── core/
│       └── config.py      # Settings/configuration

🛠️ Development Notes

The database is SQLite (fastapi.db).

SQLAlchemy models and Pydantic schemas define structure and validation.

You can extend this project by adding new routers, models, and schemas.

🔁 Database schema auto-updates (SQLite)

On startup, the app ensures the `items` table includes the following columns for backwards compatibility with older databases:

- item_type (expense | earning, default: expense)
- amount (integer, default: 0)
- date (DATE, default: current date)

If you are using an existing `fastapi.db`, these columns will be added automatically when the app starts. New databases are created with the full schema.

🧭 Endpoints overview

- Users: `/users`
  - POST `/` create, GET `/` list, GET `/{user_id}`, PUT `/{user_id}`, DELETE `/{user_id}`

- Items: `/items`
  - POST `/` create, GET `/` list, GET `/{item_id}`, PUT `/{item_id}`, DELETE `/{item_id}`
  - GET `/search` with optional filters: `owner_id`, `q` (matches title/description), `item_type` (expense|earning), `date_from`, `date_to`, `skip`, `limit`

📖 Docs

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc