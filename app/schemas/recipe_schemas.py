# /app/schemas/recipe_schemas.py

from pydantic import BaseModel, Field
from typing import Dict, Optional

class IngredientItem(BaseModel):
    id: int
    name: str

class RecipeSearchCriteria(BaseModel):
    ingredients: Dict[str, IngredientItem]
    specialRequests: Optional[str] = None

# You can also define response models here if needed
