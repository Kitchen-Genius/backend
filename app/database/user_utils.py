from .db import database

async def update_user_favorites(user_id: int, recipe_id: int, like: bool):
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
