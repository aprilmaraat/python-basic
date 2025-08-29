# from typing import Union
from fastapi import FastAPI
from app.routers import user, item
from app.db.session import engine, Base

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with SQLAlchemy", description="A simple CRUD API using FastAPI and SQLAlchemy")

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(item.router, prefix="/items", tags=["items"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Level 2 Example"}