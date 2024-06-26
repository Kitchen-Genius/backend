# recipe_processing.py
from app.services.spoonacular import search_recipes, fetch_recipe_ingredients, fetch_recipe_nutrition
from app.utils.file_utils import save_data_locally
from app.database.db_utils import cache_recipe, get_cached_recipe_by_id
from app.utils.serialize_doc import serialize_recipe_document
from typing import List, Dict

"""Processes recipe search criteria and recipes themselves, interfacing with Spoonacular API functions for recipe data."""

def prepare_recipe_search_criteria(criteria_json: List[Dict]):
    """Formats search criteria for API requests"""
    # Assuming criteria_json is a list of criteria, but we'll just use the first item for this example
    criteria = criteria_json[0] if criteria_json else {}

    # Extracting and formatting ingredients
    ingredients = criteria.get("ingridients", [])
    includeIngredients = ",".join(ingredient["name"] for ingredient in ingredients)

    # Determining the diet
    if criteria.get("Vegetarian"):
        diet = "vegetarian"
    elif not criteria.get("Vegetarian") and criteria.get("dairyFree"):
        diet = "lacto-vegetarian"
    else:
        diet = ""  # Default or empty if no conditions are met

    return {
        "diet": diet,
        "includeIngredients": includeIngredients,
    }

def process_recipe(recipe_json, ingredients_json, nutrition_json):
    """Combines recipe, ingredient, and nutrition information into a single, processed format."""
    # Assuming there's always at least one result
    recipe = recipe_json['results'][0] if recipe_json['results'] else {}
    
    calories_info = next((item for item in nutrition_json.get("nutrients", []) if item["name"] == "Calories"), None)
    calories = calories_info["amount"] if calories_info else "N/A"

    processed_recipe = {
        "vegetarian": recipe.get("vegetarian"),
        "vegan": recipe.get("vegan"),
        "glutenFree": recipe.get("glutenFree"),
        "dairyFree": recipe.get("dairyFree"),
        "veryHealthy": recipe.get("veryHealthy"),
        "readyInMinutes": recipe.get("readyInMinutes"),
        "servings": recipe.get("servings"),
        "id": recipe.get("id"),
        "title": recipe.get("title"),
        "image": recipe.get("image"),
        "analyzedInstructions": process_recipe_instructions(recipe.get("analyzedInstructions", [])),
        "ingredients": process_ingredients_to_us_measurements(ingredients_json.get("ingredients", [])),
        "Calories": calories,
    }
    
    return processed_recipe

async def process_and_save_recipes(diet="", includeIngredients="", type="", intolerances="", 
                                   instructionsRequired=True, number=5, addRecipeInformation=True, maxReadyTime=60):
    """Orchestrates recipe searches, processing, and local saving based on search criteria."""
    # Fetch recipes based on criteria
    recipes_data = await search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number, addRecipeInformation, maxReadyTime)
    
    if recipes_data is None or "results" not in recipes_data:
        return []
    
    processed_recipes = []

    for recipe in recipes_data.get("results", []):
        recipe_id = recipe.get("id")

        cached_recipe = await get_cached_recipe_by_id(recipe_id)
        if cached_recipe:
            # Use the cached recipe
            serialized_cached_recipe = serialize_recipe_document(cached_recipe)
            processed_recipes.append(serialized_cached_recipe)
            continue
        ingredients_data = await fetch_recipe_ingredients(recipe_id)
        nutrition_data = await fetch_recipe_nutrition(recipe_id)  # Fetch nutrition information
    
        # Process the recipe to include ingredients and calories
        processed_recipe = process_recipe({"results": [recipe]}, ingredients_data, nutrition_data)
        await cache_recipe(processed_recipe)
        serialized_processed_recipe = serialize_recipe_document(processed_recipe)
        processed_recipes.append(serialized_processed_recipe)
    
    # Save the processed recipes locally
    save_data_locally(processed_recipes, f"{type}_processed_recipes.json")
    
    return processed_recipes

def process_recipe_instructions(analyzedInstructions):
    """
    Process the instructions to combine all parts into one continuous set of steps,
    removing step numbers, equipment, and ingredients details.
    """
    combined_steps = []

    # Iterate through each part of the instructions (ignoring the 'name')
    for part in analyzedInstructions:
        for step in part["steps"]:
            # Add the step text to the combined_steps list
            combined_steps.append({"step": step["step"]})

    # Now, renumber the steps sequentially
    for i, step in enumerate(combined_steps, start=1):
        step["number"] = i

    # Return the processed instructions in the expected format
    return [{"steps": combined_steps}]

def process_ingredients_to_us_measurements(ingredients):
    processed_ingredients = []

    for ingredient in ingredients:
        # Extract the 'us' measurement
        us_measurement = ingredient.get('amount', {}).get('us', {})
        processed_ingredient = {
            "name": ingredient.get("name"),
            "image": ingredient.get("image"),
            "amount": us_measurement
        }
        processed_ingredients.append(processed_ingredient)

    return processed_ingredients

