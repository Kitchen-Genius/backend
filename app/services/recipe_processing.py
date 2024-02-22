# recipe_processing.py
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

def process_recipe(recipe_json, ingredients_json):
    # Assuming there's always at least one result
    recipe = recipe_json['results'][0] if recipe_json['results'] else {}
    
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
        "ingredients": ingredients_json.get("ingredients", [])
    }
    
    return processed_recipe