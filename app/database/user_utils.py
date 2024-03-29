from .db import database

"""Provides functions specifically for managing user-related data, such as updating a user's favorite recipes list"""

async def update_user_favorites(user_id: int, recipe_id: int, like: bool):
    """Adds or removes a recipe ID to/from a user's favorites list, based on the provided like boolean flag."""
    user_collection = database.get_collection("users") 
    user = await user_collection.find_one({"user_id": user_id})
    if not user:
        return False  # User not found
    
    if like:
        # Add recipe_id to favorites if not already present
        if recipe_id not in user.get("favorites", []):
            await user_collection.update_one({"user_id": user_id}, {"$push": {"favorites": recipe_id}})
    else:
        # Remove recipe_id from favorites
        await user_collection.update_one({"user_id": user_id}, {"$pull": {"favorites": recipe_id}})
    
    return True
