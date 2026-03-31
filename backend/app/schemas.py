from pydantic import BaseModel
from typing import Optional, List


class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: str
    is_vegetarian: bool
    cook_time_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    
class RecipeUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: str
    is_vegetarian: bool
    cook_time_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    


class AIRecipeRequest(BaseModel):
    is_vegetarian: bool
    ingredients: List[str]


class AIRecipeItem(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: str
    cook_time_minutes: int
    difficulty: str


class AIRecipeResponse(BaseModel):
    recipes: List[AIRecipeItem]