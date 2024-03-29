# /app/database/db_utils.py
from .db import database
from app.services.spoonacular import fetch_recipe_information
from app.utils.serialize_doc import serialize_recipe_document
from fastapi import HTTPException

"""Contains utility functions to interact with the database, 
such as fetching cached recipes, caching new recipes, and retrieving user favorites"""

async def get_cached_recipe_by_id(recipe_id: int):
    """Fetches a recipe by ID from the cached recipes collection and serializes it for response."""
    recipe = await database.saved_recipes.find_one({"id": recipe_id})
    if recipe:
        return serialize_recipe_document(recipe)
    return None

async def cache_recipe(recipe):
    """Caches a recipe document in the database if it doesn’t exist."""
    existing_recipe = await get_cached_recipe_by_id(recipe['id'])
    if not existing_recipe:
        await database.saved_recipes.insert_one(recipe)

def extract_required_recipe_info(recipe_document):
    """Extracts and returns only the necessary fields (id, title, image) from a recipe document."""
    return {
        "id": recipe_document["id"],
        "title": recipe_document.get("title", "No Title"),
        "image": recipe_document.get("image", "No Image Available")
    }

async def get_user_favorites(user_id: int):
    """Retrieves a user's favorite recipes list, fetching recipe details from cache or Spoonacular API as needed."""
    user = await database.users.find_one({"user_id": user_id})
    if not user or "favorites" not in user:
        return []

    favorite_recipes = []
    for recipe_id in user["favorites"]:
        actual_recipe_id = int(recipe_id)
        cached_recipe = await database.saved_recipes.find_one({"id": actual_recipe_id})
        if cached_recipe:
            # Extract and append the required information from the cached recipe
            favorite_recipes.append(extract_required_recipe_info(cached_recipe))
        else:
            # If not cached, fetch from Spoonacular, cache, and then append required info
            try:
                recipe_info = await fetch_recipe_information(actual_recipe_id)
                favorite_recipes.append(extract_required_recipe_info(recipe_info))
            except HTTPException as e:
                print(f"Failed to fetch recipe {actual_recipe_id} from Spoonacular: {e.detail}")
                continue  # Skip if the recipe couldn't be fetched

    return favorite_recipes