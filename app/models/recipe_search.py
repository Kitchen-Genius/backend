# /app/models/recipe_search.py
from typing import List
from pydantic import BaseModel, Field

"""Defines models received from frontend for searching recipes."""


class RecipeSearchRequest(BaseModel):
    """Defines the criteria for searching recipes based on healthiness, calorie content, 
    dietary restrictions, ingredients, and meal type (breakfast, lunch, dinner). 
    Includes a CookingTime field for specifying the maximum acceptable cooking time."""
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
    CookingTime: int = Field(None, alias="CookingTime", description="Maximum cooking time in minutes")