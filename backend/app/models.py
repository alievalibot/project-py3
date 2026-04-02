from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from app.database import Base
from datetime import datetime

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(Text, nullable = True)
    instructions = Column(Text, nullable = False)
    is_vegetarian = Column(Boolean, default = False)
    cook_time_minutes = Column(Integer, nullable = True)
    difficulty = Column(String, nullable = True)
    
class GenerationRequest(Base):
    __tablename__ = "generation_requests"

    id = Column(Integer, primary_key=True, index=True)
    is_vegetarian = Column(Boolean, nullable=False)
    ingredients = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)