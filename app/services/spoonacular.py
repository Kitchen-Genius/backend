import httpx
import requests
import os
from dotenv import load_dotenv
from app.utils.file_utils import save_data_locally
from app.utils.validations import validate_params


load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

## TODO allow searching with empty diet, type and intolerances: ##
async def search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired=True, number=1, addRecipeInformation=True):
    if not validate_params('diets', diet, 'diets') or not validate_params('meal_types', type, 'meal_types') or not validate_params('intolerances', intolerances, 'intolerances'):
        return {"error": "Invalid diet, type, or intolerance parameter"}

    url = "https://api.spoonacular.com/recipes/complexSearch"
    query = {
        "apiKey": API_KEY,
        "diet": diet,
        "includeIngredients": includeIngredients,
        "type": type,
        "intolerances": intolerances,
        "instructionsRequired": instructionsRequired,
        "number": number,
        "addRecipeInformation": addRecipeInformation,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=query)
    data = response.json()

    # Save the response locally
    save_data_locally(data, f"{type}_recipes.json")
    
    return data

async def fetch_recipe_ingredients(recipe_id: int):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/ingredientWidget.json"
    params = {"apiKey": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors or unexpected responses
        return {"error": "Failed to fetch recipe ingredients", "status_code": response.status_code}

def get_analyzed_recipe_instructions(id, stepBreakdown=True):
    if not isinstance(id, int):
        return {"error": "Invalid recipe ID"}

    url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"
    query = {
        "apiKey": API_KEY,
        "stepBreakdown": stepBreakdown
    }
    response = requests.get(url, params=query)
    data = response.json()

    # Save the response locally
    save_data_locally(data, f"recipe_{id}_instructions.json")
    
    return data

async def fetch_recipe_nutrition(recipe_id: int):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch recipe nutrition", "status_code": response.status_code}
