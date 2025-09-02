# from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, item
from app.db.session import engine, Base
 

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with SQLAlchemy", description="A simple CRUD API using FastAPI and SQLAlchemy")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(item.router, prefix="/items", tags=["items"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Level 2 Example"}