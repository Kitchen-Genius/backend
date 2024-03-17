from app.services.recipe_processing import process_and_save_recipes
from app.models.recipe_search_criteria import RecipeSearchCriteria
from app.database.db_utils import get_cached_recipe_by_id, cache_recipe, get_user_favorites
from app.services.spoonacular import fetch_recipe_information
from app.utils.serialize_doc import serialize_recipe_document

async def process_search_criteria(criteria: RecipeSearchCriteria) -> str:
    # Convert ingredients list to a comma-separated string
    ingredients_str = ",".join(criteria.ingredients)
    
    # Determine diet based on Vegetarian flag
    diet = "vegetarian" if criteria.Vegetarian else ""
    
    # Determine intolerances based on Gluten_free flag
    intolerances = "gluten" if criteria.Gluten_free else ""
    
    # Call the function to search and save recipes
    recipes = await process_and_save_recipes(diet=diet, includeIngredients=ingredients_str, intolerances=intolerances)
    
    return recipes

async def get_favorite_recipes(user_id: int):
    favorite_recipe_ids = await get_user_favorites(user_id)
    favorite_recipes = []

    for recipe_id in favorite_recipe_ids:
        recipe = await get_cached_recipe_by_id(recipe_id)
        if not recipe:
            # Fetch from Spoonacular and cache it
            recipe = await fetch_recipe_information(recipe_id)
            await cache_recipe(recipe)
        # Process and serialize recipe document
        processed_recipe = serialize_recipe_document({
            "id": recipe.get("id"),
            "title": recipe.get("title"),
            "image": recipe.get("image")
        })
        favorite_recipes.append(processed_recipe)

    return favorite_recipes