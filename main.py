# from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, item
from app.db.session import engine, Base
from sqlalchemy import text

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Ensure schema is in sync for existing SQLite DBs
with engine.connect() as conn:
    # Add missing column `item_type` on `items` if upgrading an old DB
    try:
        # Use driver-level SQL to avoid SQLAlchemy parsing quirks with PRAGMA
        result = conn.exec_driver_sql("PRAGMA table_info(items);")
        columns = [row[1] for row in result]
        if "item_type" not in columns:
            conn.exec_driver_sql(
                "ALTER TABLE items ADD COLUMN item_type VARCHAR(20) NOT NULL DEFAULT 'expense'"
            )
            conn.commit()
        if "amount" not in columns:
            conn.exec_driver_sql(
                "ALTER TABLE items ADD COLUMN amount INTEGER NOT NULL DEFAULT 0"
            )
            conn.commit()
        if "date" not in columns:
            conn.exec_driver_sql(
                "ALTER TABLE items ADD COLUMN date DATE NOT NULL DEFAULT (CURRENT_DATE)"
            )
            conn.commit()
    except Exception:
        # If the table doesn't exist yet, create_all above will create it
        pass

app = FastAPI(title="FastAPI with SQLAlchemy", description="A simple CRUD API using FastAPI and SQLAlchemy")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(item.router, prefix="/items", tags=["items"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Level 2 Example"}