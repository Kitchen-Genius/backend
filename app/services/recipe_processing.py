# recipe_processing.py
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