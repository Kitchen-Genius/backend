from pydantic import BaseModel

"""Models for handling requests related to user favorites."""



class FavoriteRecipeRequest(BaseModel):
    """Captures the data for adding or removing a recipe from a user's favorites. 
    It includes the user's ID, the recipe's ID, and a boolean indicating whether the recipe should be liked or unliked."""
    user_id: int
    recipe_id: int
    like: bool



class UserFavoriteRequest(BaseModel):
    """Used for requests to fetch a user's favorite recipes, identified by the user's ID."""
    user_id: int