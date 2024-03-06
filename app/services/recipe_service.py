from typing import Tuple
from app.services.recipe_processing import process_and_save_recipes
from app.models.recipe_search_criteria import RecipeSearchCriteria

async def process_search_criteria(criteria: RecipeSearchCriteria) -> str:
    # Convert ingredients list to a comma-separated string
    ingredients_str = ",".join(criteria.ingredients)
    
    # Determine diet based on Vegetarian flag
    diet = "vegetarian" if criteria.Vegetarian else ""
    
    # Determine intolerances based on Gluten_free flag
    intolerances = "gluten" if criteria.Gluten_free else ""
    
    # Call the function to search and save recipes (assuming it's already defined)
    recipes = await process_and_save_recipes(diet=diet, includeIngredients=ingredients_str, intolerances=intolerances)
    
    return recipes
