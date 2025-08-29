from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True, nullable=False)
    # username = Column(String, unique=True, nullable=False)
    username = Column(String(191), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="owner")