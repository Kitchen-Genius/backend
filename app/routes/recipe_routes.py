from fastapi import APIRouter, Depends, Body, HTTPException
from pymongo import MongoClient
import logging
from app.services import spoonacular as spoonacular_service
from app.database.db_utils import get_cached_recipe_by_id
from app.services.recipe_processing import process_and_save_recipes, prepare_recipe_search_criteria
from app.utils.validations import validate_diet, validate_type, validate_intolerances
from app.models.recipe_models import ProcessRecipesCriteria
from app.models.recipe_search import RecipeSearchRequest
from app.services.recipe_service import process_and_save_recipes


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


router = APIRouter()


@router.get("/search-recipes/")
async def search_recipes(
        diet: str = Depends(validate_diet),
        includeIngredients: str = None,
        type: str = Depends(validate_type),
        intolerances: str = Depends(validate_intolerances),
        instructionsRequired: bool = True,
        addRecipeInformation: bool = True,
        maxReadyTime: int = 20,
        number: int = 1

):
    data = await spoonacular_service.search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired,
                                                    number, addRecipeInformation, maxReadyTime)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return {"results": []}


@router.get("/recipes/")
async def get_recipes(
        diet: str = Depends(validate_diet),
        includeIngredients: str = None,
        type: str = Depends(validate_type),
        intolerances: str = Depends(validate_intolerances),
        instructionsRequired: bool = True,
        number: int = 1
):
    try:
        recipes = await spoonacular_service.search_recipes(diet=diet, includeIngredients=includeIngredients, type=type,
                                                           intolerances=intolerances,
                                                           instructionsRequired=instructionsRequired, number=number)
        return recipes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/processed-recipes/")
async def get_processed_recipes(
        diet: str = Depends(validate_diet),
        includeIngredients: str = None,
        type: str = Depends(validate_type),
        intolerances: str = Depends(validate_intolerances),
        instructionsRequired: bool = True,
        addRecipeInformation: bool = True,
        maxReadyTime: int = 20,
        number: int = 1

):
    try:
        processed_recipes = await process_and_save_recipes(diet=diet, includeIngredients=includeIngredients, type=type,
                                                           intolerances=intolerances,
                                                           instructionsRequired=instructionsRequired, number=number,
                                                           addRecipeInformation=addRecipeInformation,
                                                           maxReadyTime=maxReadyTime)
        return processed_recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/process-recipes-criteria")
async def process_recipes_criteria(criteria: ProcessRecipesCriteria = Body(...)):
    try:
        processed_recipes_list = []
        for criteria_set in criteria.criteria:
            criteria_dict = criteria_set.model_dump()
            search_criteria = prepare_recipe_search_criteria([criteria_dict])  # Adjust if your logic expects a list
            processed_recipes = await process_and_save_recipes(
                diet=search_criteria["diet"],
                includeIngredients=search_criteria["includeIngredients"],
                type=criteria_dict.get("type", ""),
                intolerances=criteria_dict.get("intolerances", ""),
                instructionsRequired=criteria_dict.get("instructionsRequired", True),
                number=criteria_dict.get("number", 10)
            )
            processed_recipes_list.append(processed_recipes)

        return processed_recipes_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/atlas/save_recipe")
async def save_recipe(user_id: str, recipe_id: str, state: bool):
    try:
        # Check if the user exists in the collection
        user_data = collection.find_one({"User": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        # Update the user's saved list based on the state
        if state:
            # If state is true, push the recipe_id into the saved_list
            collection.update_one(
                {"User": user_id},
                {"$addToSet": {"saved_list": recipe_id}}
            )
        else:
            # If state is false, remove the recipe_id from the saved_list
            collection.update_one(
                {"User": user_id},
                {"$pull": {"saved_list": recipe_id}}
            )

        return {"message": "Recipe saved successfully", "user_id": user_id, "recipe_id": recipe_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/atlas/save_recipe")
async def save_recipe(user_id: str, recipe_id: str, state: bool):
    try:
        # Check if the user exists in the collection
        user_data = collection.find_one({"user_id": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        # Update the user's saved list based on the state
        if state:
            # If state is true, push the recipe_id into the saved_list
            collection.update_one(
                {"user_id": user_id},
                {"$addToSet": {"saved_list": recipe_id}}
            )
        else:
            # If state is false, remove the recipe_id from the saved_list
            collection.update_one(
                {"user_id": user_id},
                {"$pull": {"saved_list": recipe_id}}
            )

        return {"message": "Recipe saved successfully", "user_id": user_id, "recipe_id": recipe_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/atlas/get_recipes/{user_id}")
async def get_recipes(user_id: str):
    try:
        # Check if the user exists in the 'collection'
        user_data = collectionUsers.find_one({"user_id": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        # Retrieve the user's saved list of recipe IDs
        saved_list = user_data.get("saved_list", [])

        # Assuming you have a separate collection for recipes
        recipes_collection = db["saved_recipes"]

        # Retrieve the recipes from 'recipes_collection' based on the saved_list
        recipes = recipes_collection.find({"recipe_id": {"$in": saved_list}})

        # Return the recipes from the user's saved list
        return {"user_id": user_id, "saved_recipes": list(recipes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipe = await get_cached_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("/recipes/search")
async def post_search_recipes(request_body: RecipeSearchRequest):
    ingredients = ",".join(request_body.ingredients)
    diet = "vegetarian" if request_body.Vegetarian else ""
    intolerances = "gluten" if request_body.Gluten_free else ""

    try:
        recipes = await process_and_save_recipes(
            diet=diet,
            includeIngredients=ingredients,
            intolerances=intolerances
        )
        return recipes
    except Exception as e:
        logging.error(f"Failed to process and save recipes: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=str(e) or "An internal error occurred.")