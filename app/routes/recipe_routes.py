from fastapi import APIRouter, Depends, Body, HTTPException
from pymongo import MongoClient
import logging
from app.services import spoonacular as spoonacular_service
from app.database.db_utils import get_cached_recipe_by_id
from app.services.recipe_processing import process_and_save_recipes, prepare_recipe_search_criteria
from app.utils.validations import validate_diet, validate_type, validate_intolerances
from app.models.recipe_models import ProcessRecipesCriteria, RecipeIDRequest
from app.models.recipe_search import RecipeSearchRequest
from app.services.recipe_service import process_and_save_recipes
from app.services.recipe_management import fetch_and_cache_recipe


MONGODB_URI = "mongodb+srv://KGUser:jXH2M8loFrZjtSYR@cluster0.v1oaihv.mongodb.net/"
DATABASE_NAME = "KitchenGenius"
COLLECTION_NAME = "saved_recipies"
COLLECTION_USERS = "users"

# Create a MongoClient instance
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
collectionUsers = db[COLLECTION_USERS]

router = APIRouter()


class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

@router.post("/recipes/search")
async def post_search_recipes(request_body: RecipeSearchRequest):
    ingredients = ",".join(request_body.ingredients)
    diet = "vegetarian" if request_body.Vegetarian else ""
    intolerances = "gluten" if request_body.Gluten_free else ""
    cooking_time = request_body.CookingTime

    try:
        recipes = await process_and_save_recipes(
            diet=diet,
            includeIngredients=ingredients,
            intolerances=intolerances,
            maxReadyTime=cooking_time
        )
        return recipes
    except Exception as e:
        logging.error(f"Failed to process and save recipes: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=str(e) or "An internal error occurred.")
    
@router.post("/recipes/{recipe_id}")
async def get_recipe_by_id(request: RecipeIDRequest):
    try:
        recipe = await fetch_and_cache_recipe(request.recipe_id)
        return recipe
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")