# app/routes/ingredients_routes.py
from fastapi import APIRouter, HTTPException
from app.database.db import ingredients_collection  # Adjust import path as necessary

router = APIRouter()

@router.get("/ingredient/{ingredient_name}")
async def get_ingredient(ingredient_name: str):
    print(f"Searching for ingredient: {ingredient_name}")
    ingredient = await ingredients_collection.find_one({"name": ingredient_name})
    print(f"Found ingredient: {ingredient}")
    if ingredient is not None:
        return ingredient
    else:
        raise HTTPException(status_code=404, detail="Ingredient not found")