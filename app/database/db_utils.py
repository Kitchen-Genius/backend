# /app/database/db_utils.py
from .db import database
from app.services.spoonacular import fetch_recipe_information
from app.utils.serialize_doc import serialize_recipe_document
from fastapi import HTTPException

async def get_cached_recipe_by_id(recipe_id: int):
    recipe = await database.saved_recipes.find_one({"id": recipe_id})
    return recipe

async def cache_recipe(recipe):
    existing_recipe = await get_cached_recipe_by_id(recipe['id'])
    if not existing_recipe:
        await database.saved_recipes.insert_one(recipe)

async def get_user_favorites(user_id: int):
    user = await database.users.find_one({"user_id": user_id})
    if not user or "favorites" not in user:
        return []

    favorite_recipes = []
    for recipe_id in user["favorites"]:
        # Try to get the cached recipe first
        cached_recipe = await database.saved_recipes.find_one({"id": recipe_id})
        if cached_recipe:
            favorite_recipes.append(serialize_recipe_document(cached_recipe))
        else:
            # If not cached, fetch from Spoonacular and cache
            try:
                recipe_info = await fetch_recipe_information(recipe_id)
                favorite_recipes.append(recipe_info)
            except HTTPException:
                continue  # Skip if the recipe couldn't be fetched

    return favorite_recipes