from fastapi import APIRouter, Body, HTTPException
from app.models.request_models import FavoriteRecipeRequest
from app.database.user_utils import update_user_favorites  
from app.services.recipe_management import fetch_user_favorite_recipes

"""Manages endpoints related to user-specific functionalities 
like updating favorites and fetching a user's favorite recipes list"""

router = APIRouter()

@router.post("/users/favorites")
async def update_favorites(request: FavoriteRecipeRequest):
    """Adds or removes a recipe from a user's favorites list based on the like parameter"""
    try:
        updated = await update_user_favorites(request.user_id, request.recipe_id, request.like)
        if updated:
            return {"message": "User's favorites updated successfully"}
        else:
            return {"message": "User or recipe not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users/favorites/list")
async def fetch_user_favorites(user_id: int = Body(..., embed=True)):
    """Retrieves a list of a user's favorite recipes, including only the necessary details like ID, 
    title, and image."""
    try:
        favorites = await fetch_user_favorite_recipes(user_id)
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))