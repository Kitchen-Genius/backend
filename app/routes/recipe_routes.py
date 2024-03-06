from fastapi import APIRouter, Depends, HTTPException
from app.services import spoonacular as spoonacular_service
from app.services.recipe_processing import process_and_save_recipes
from app.utils.validations import validate_diet, validate_type, validate_intolerances
from app.schemas.recipe_schemas import RecipeSearchCriteria
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
    addRecipeInformation: bool = True,
    maxReadyTime: int = 20,
    number: int = 1

):
    data = await spoonacular_service.search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number, addRecipeInformation, maxReadyTime )
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

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
    addRecipeInformation: bool = True,
    maxReadyTime: int = 20,
    number: int = 1
    
):
    try:
        processed_recipes = await process_and_save_recipes(diet=diet, includeIngredients=includeIngredients, type=type, intolerances=intolerances, instructionsRequired=instructionsRequired, number=number, addRecipeInformation=addRecipeInformation, maxReadyTime=maxReadyTime)
        return processed_recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/process-recipes-criteria")
async def process_recipe_criteria(criteria: RecipeSearchCriteria):
    # Convert the ingredients dictionary to a comma-separated list of ingredient names
    includeIngredients = ",".join(criteria.ingredients.values())

    # Call your function to search for recipes with the processed ingredients and any special requests
    # This is a placeholder for whatever logic you use to interact with the recipe API
    try:
        recipe_results = await search_recipes(
            diet="",  # You'll need to adjust how you handle diets, types, and intolerances based on the frontend data
            includeIngredients=includeIngredients,
            type="",  # Adjust accordingly
            intolerances="",  # Adjust accordingly
            instructionsRequired=True,
            number=10  # Example, adjust as needed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recipes: {str(e)}")

    # Return the recipe results to the frontend
    return recipe_results
    



# @router.post("/atlas/save_recipe")
# async def save_recipe(recipe: RecipeCriteria = Body(...)):
#     try:
#         # collection.insert_one(
#         #     {"User": recipe["user"]},
#         #     {"$set": {"recipeCollectio": recipe }}
#         # )
#         result = collection.insert_one(recipe)
#         return {"message": "Recipe saved successfully", "id": str(result.inserted_id)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/atlas/get_recipes")
async def get_recipes():
    try:
        recipes = collection.find()
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




