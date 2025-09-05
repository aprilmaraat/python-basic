from sqlalchemy import Column, Integer, String, ForeignKey, Date, text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, index=True, server_default=text('CURRENT_DATE'))
    owner_id = Column(Integer, ForeignKey("users.id"))
    # "expense" or "earning"
    item_type = Column(String(20), nullable=False, index=True, default="expense")
    

    owner = relationship("User", back_populates="items")