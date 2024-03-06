# /app/models/recipe_search.py
from typing import List
from pydantic import BaseModel

class RecipeSearchRequest(BaseModel):
    veryHealthy: bool = False
    Low_calories: bool = False
    dairyFree: bool = False
    Gluten_free: bool = False
    Vegetarian: bool = False
    High_protein: bool = False
    ingredients: List[str] = []
    breakfast: bool = False
    lunch: bool = False
    dinner: bool = False
