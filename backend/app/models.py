from sqlalchemy import Boolean, Column, Integer, String, Text
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(Text, nullable = True)
    instructions = Column(Text, nullable = False)
    is_vegetarian = Column(Boolean, default = False)
    cook_time_minutes = Column(Integer, nullable = True)
    difficulty = Column(String, nullable = True)