from fastapi import APIRouter, Depends, Body, HTTPException
from app.services import spoonacular as spoonacular_service
from app.services.recipe_processing import process_and_save_recipes, prepare_recipe_search_criteria
from app.utils.validations import validate_diet, validate_type, validate_intolerances
from app.models.recipe_models import ProcessRecipesCriteria
from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://KGUser:jXH2M8loFrZjtSYR@cluster0.v1oaihv.mongodb.net/"
DATABASE_NAME = "KitchenGenius"
COLLECTION_NAME = "saved_recipies"
# Provide the connection details
hostname = 'cluster0.v1oaihv.mongodb.net'
port = 27017  # Default MongoDB port
username = 'KGUser'  # If authentication is required
password = 'jXH2M8loFrZjtSYR'  # If authentication is required

# Create a MongoClient instance

client = MongoClient(MONGODB_URI )
print("#####################")
print(client)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

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
    number: int = 1
):
    data = await spoonacular_service.search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

@router.get("/processed-recipes/")
async def get_processed_recipes(
    diet: str = Depends(validate_diet), 
    includeIngredients: str = None, 
    type: str = Depends(validate_type), 
    intolerances: str = Depends(validate_intolerances)
):
    processed_recipes = await spoonacular_service(diet, includeIngredients, type, intolerances)
    if "error" in processed_recipes:
        raise HTTPException(status_code=400, detail=processed_recipes["error"])
    return processed_recipes

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
        recipes = await spoonacular_service.search_recipes(diet=diet, includeIngredients=includeIngredients, type=type, intolerances=intolerances, instructionsRequired=instructionsRequired, number=number)
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
    number: int = 1
):
    try:
        processed_recipes = await process_and_save_recipes(diet=diet, includeIngredients=includeIngredients, type=type, intolerances=intolerances, instructionsRequired=instructionsRequired, number=number)
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
async def save_recipe(recipe: dict = Body(...)):
    try:
        # collection.insert_one(
        #     {"User": recipe["user"]},
        #     {"$set": {"recipeCollectio": recipe }}
        # )
        result = collection.insert_one(recipe)
        return {"message": "Recipe saved successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/atlas/get_recipes")
async def get_recipes():
    try:
        recipes = collection.find()
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




