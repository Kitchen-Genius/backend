from pydantic import BaseModel

class FavoriteRecipeRequest(BaseModel):
    user_id: int
    recipe_id: int
    like: bool
