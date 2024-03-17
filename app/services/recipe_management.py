# app/services/recipe_management.py

from .spoonacular import fetch_recipe_information
from app.database.db_utils import cache_recipe, get_cached_recipe_by_id, get_user_favorites

async def fetch_and_cache_recipe(recipe_id: int):
    # First, attempt to get the recipe from cache
    cached_recipe = await get_cached_recipe_by_id(recipe_id)
    if cached_recipe:
        return cached_recipe

    # If not cached, fetch from Spoonacular
    recipe_info = await fetch_recipe_information(recipe_id)
    # Cache the fetched recipe
    await cache_recipe(recipe_info)
    return recipe_info

async def fetch_user_favorite_recipes(user_id: int):
    favorite_recipes_info = await get_user_favorites(user_id)
    return favorite_recipes_info