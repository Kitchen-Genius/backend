from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Ingredient(BaseModel):
    id: int
    name: str

class RecipeSearchCriteria(BaseModel):
    High_protein: Optional[bool] = None
    Low_calories: Optional[bool] = None
    Vegetarian: Optional[bool] = None
    dairyFree: Optional[bool] = None
    breakfast: Optional[bool] = None
    lunch: Optional[bool] = None
    dinner: Optional[bool] = None
    dessert: Optional[bool] = None
    levelOfCooking: Optional[str] = None
    ingredients: List[Ingredient] = []

@app.post("/api/saveIngredients")
async def save_ingredients(criteria: RecipeSearchCriteria):
    # Here you would process the received data
    # For example, converting criteria and ingredients into a search query for recipes
    # Then, fetching those recipes from an external API or database
    print(criteria)  # For demonstration purposes

    # Placeholder response
    return {"message": "Received and processed search criteria", "data": criteria}
