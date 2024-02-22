from fastapi import APIRouter, HTTPException
from app.services import spoonacular as spoonacular_service

router = APIRouter()

@router.get("/search-recipes/")
async def search_recipes(diet: str, includeIngredients: str, type: str, intolerances: str, instructionsRequired: bool = True, number: int = 1):
    data = await spoonacular_service.search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

@router.get("/processed-recipes/")
async def get_processed_recipes(diet: str, includeIngredients: str, type: str, intolerances: str):
    processed_recipes = await spoonacular_service(diet, includeIngredients, type, intolerances)
    return processed_recipes