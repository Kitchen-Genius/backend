from fastapi import APIRouter, HTTPException
from app.models.request_models import FavoriteRecipeRequest
from app.database.user_utils import update_user_favorites  

router = APIRouter()

@router.post("/users/favorites")
async def update_favorites(request: FavoriteRecipeRequest):
    try:
        updated = await update_user_favorites(request.user_id, request.recipe_id, request.like)
        if updated:
            return {"message": "User's favorites updated successfully"}
        else:
            return {"message": "User or recipe not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
