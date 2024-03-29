import httpx
import requests
import os
from dotenv import load_dotenv
from app.utils.file_utils import save_data_locally
from app.utils.serialize_doc import serialize_recipe_document
from app.utils.validations import validate_params
from fastapi import HTTPException

"""Interfaces with the Spoonacular API to fetch recipe information, ingredients, nutrition, and specific recipe data."""

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

async def search_recipes(diet='', includeIngredients='', type='', intolerances='', instructionsRequired=True, number=1, addRecipeInformation=True, maxReadyTime=20):
    """Searches for recipes based on specified criteria"""
    if diet and not validate_params('diets', diet, 'diets'):
        return {"error": "Invalid diet parameter"}
    if type and not validate_params('meal_types', type, 'meal_types'):
        return {"error": "Invalid type parameter"}
    if intolerances and not validate_params('intolerances', intolerances, 'intolerances'):
        return {"error": "Invalid intolerances parameter"}

    url = "https://api.spoonacular.com/recipes/complexSearch"
    query = {
        "apiKey": API_KEY,
        "instructionsRequired": instructionsRequired,
        "number": number,
        "addRecipeInformation": addRecipeInformation,
        "maxReadyTime": maxReadyTime,
    }
    # Conditionally add parameters if they are not empty
    if diet != "":
        query["diet"] = diet
    if includeIngredients:
        query["includeIngredients"] = includeIngredients
    if type != "":
        query["type"] = type
    if intolerances != "":
        query["intolerances"] = intolerances

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=query)
    data = response.json()

    # Save the response locally
    save_data_locally(data, f"{type}_recipes.json")
    
    return data

async def fetch_recipe_ingredients(recipe_id: int):
    """Fetch ingredients of a recipe by ID"""
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
    """Fetch analyzed instructions of a recipe by ID"""
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
    """Fetch nutrition of a recipe by ID"""
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch recipe nutrition", "status_code": response.status_code}

async def fetch_recipe_information(recipe_id: int):
    """Retrieves comprehensive information about a recipe, including optional nutrition data."""
    API_KEY = os.getenv("SPOONACULAR_API_KEY")
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=false"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            recipe_data = response.json()
            # Process the recipe
            processed_recipe = serialize_recipe_document(recipe_data)
            return processed_recipe
        else:
            raise HTTPException(status_code=404, detail="Recipe not found in Spoonacular API.")
