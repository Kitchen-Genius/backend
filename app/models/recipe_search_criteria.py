from pydantic import BaseModel
from typing import List, Optional

class RecipeSearchCriteria(BaseModel):
    veryHealthy: Optional[bool] = False
    Low_calories: Optional[bool] = False
    dairyFree: Optional[bool] = False
    Gluten_free: Optional[bool] = False
    Vegetarian: Optional[bool] = False
    High_protein: Optional[bool] = False
    ingredients: List[str] = []
    breakfast: Optional[bool] = False
    lunch: Optional[bool] = False
    dinner: Optional[bool] = False
