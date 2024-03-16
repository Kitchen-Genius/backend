# /app/database/db_utils.py
from .db import database

async def get_cached_recipe_by_id(recipe_id: int):
    recipe = await database.saved_recipes.find_one({"id": recipe_id})
    return recipe

async def cache_recipe(recipe):
    existing_recipe = await get_cached_recipe_by_id(recipe['id'])
    if not existing_recipe:
        await database.saved_recipes.insert_one(recipe)
