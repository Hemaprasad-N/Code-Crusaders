from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    tamil_text = Column(String(500))
    english_text = Column(String(500))
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
