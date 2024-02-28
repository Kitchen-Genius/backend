# recipe_processing.py
from app.services.spoonacular import search_recipes, fetch_recipe_ingredients, fetch_recipe_nutrition
from app.utils.file_utils import save_data_locally
from typing import List, Dict

def prepare_recipe_search_criteria(criteria_json: List[Dict]):
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
        "id": recipe.get("id"),
        "title": recipe.get("title"),
        "image": recipe.get("image"),
        "analyzedInstructions": recipe.get("analyzedInstructions"),
        "ingredients": ingredients_json.get("ingredients", []),
        "Calories": calories,
    }
    
    return processed_recipe

async def process_and_save_recipes(diet="", includeIngredients="", type="", intolerances="", instructionsRequired=True, number=10):
    # Fetch recipes based on criteria
    recipes_data = await search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number, addRecipeInformation=True)
    processed_recipes = []

    for recipe in recipes_data.get("results", []):
        recipe_id = recipe.get("id")
        ingredients_data = await fetch_recipe_ingredients(recipe_id)
        nutrition_data = await fetch_recipe_nutrition(recipe_id)  # Fetch nutrition information
        
        # Process the recipe to include ingredients and calories
        processed_recipe = process_recipe({"results": [recipe]}, ingredients_data, nutrition_data)
        processed_recipes.append(processed_recipe)
    
    # Save the processed recipes locally
    save_data_locally(processed_recipes, f"{type}_processed_recipes.json")
    
    return processed_recipes