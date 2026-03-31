import os
import json
from google import genai
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import Base, engine
from app.models import Recipe
from app import schemas
from typing import Optional
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def root():
    return {"message": "Cooking API is running"}


@app.get("/test-db")
def test_db():
    with Session(engine) as session:
        session.execute(text("SELECT 1"))
        return {"message": "Database connection works"}


@app.post("/recipes")
def create_recipe(recipe: schemas.RecipeCreate):
    with Session(engine) as session:
        new_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            instructions=recipe.instructions,
            is_vegetarian=recipe.is_vegetarian,
            cook_time_minutes=recipe.cook_time_minutes,
            difficulty=recipe.difficulty
        )

        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)

        return {
            "id": new_recipe.id,
            "title": new_recipe.title,
            "description": new_recipe.description,
            "instructions": new_recipe.instructions,
            "is_vegetarian": new_recipe.is_vegetarian,
            "cook_time_minutes": new_recipe.cook_time_minutes,
            "difficulty": new_recipe.difficulty
        }
        

@app.get("/recipes")
def get_recipes(
    vegetarian: Optional[bool] = None,
    search: Optional[str] = None
):
    with Session(engine) as session:
        query = session.query(Recipe)

        if vegetarian is not None:
            query = query.filter(Recipe.is_vegetarian == vegetarian)

        if search:
            query = query.filter(Recipe.title.ilike(f"%{search}%"))

        recipes = query.all()

        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "instructions": recipe.instructions,
                "is_vegetarian": recipe.is_vegetarian,
                "cook_time_minutes": recipe.cook_time_minutes,
                "difficulty": recipe.difficulty
            }
            for recipe in recipes
        ]
        
@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "is_vegetarian": recipe.is_vegetarian,
            "cook_time_minutes": recipe.cook_time_minutes,
            "difficulty": recipe.difficulty
        }
        
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        session.delete(recipe)
        session.commit()

        return {"message": "Recipe deleted successfully"}
    
    
@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, updated_recipe: schemas.RecipeUpdate):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        recipe.title = updated_recipe.title
        recipe.description = updated_recipe.description
        recipe.instructions = updated_recipe.instructions
        recipe.is_vegetarian = updated_recipe.is_vegetarian
        recipe.cook_time_minutes = updated_recipe.cook_time_minutes
        recipe.difficulty = updated_recipe.difficulty

        session.commit()
        session.refresh(recipe)

        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "is_vegetarian": recipe.is_vegetarian,
            "cook_time_minutes": recipe.cook_time_minutes,
            "difficulty": recipe.difficulty
        }
        
@app.post("/ai-recipes", response_model=schemas.AIRecipeResponse)
def generate_ai_recipes(data: schemas.AIRecipeRequest):
    vegetarian_text = "vegetarian" if data.is_vegetarian else "not necessarily vegetarian"
    ingredients_text = ", ".join(data.ingredients)

    prompt = f"""
You are a cooking assistant.

Generate exactly 3 recipe ideas for a user.

User preference: {vegetarian_text}
Available ingredients: {ingredients_text}

Return ONLY valid JSON.
Do not add markdown.
Do not use ```json.
Do not write explanations.

Use exactly this format:
{{
  "recipes": [
    {{
      "title": "string",
      "description": "string",
      "ingredients": ["string", "string"],
      "instructions": "string",
      "cook_time_minutes": 20,
      "difficulty": "easy"
    }}
  ]
}}

Rules:
- If the user is vegetarian, do not include meat or fish.
- Base the recipes primarily on the provided ingredients.
- You may include a few common pantry items if needed.
- Keep recipes realistic and simple.
- difficulty must be one of: easy, medium, hard.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text_output = response.text.strip()

        if text_output.startswith("```json"):
            text_output = text_output.removeprefix("```json").strip()
        if text_output.startswith("```"):
            text_output = text_output.removeprefix("```").strip()
        if text_output.endswith("```"):
            text_output = text_output.removesuffix("```").strip()

        parsed = json.loads(text_output)
        return parsed

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini returned invalid JSON: {text_output}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))