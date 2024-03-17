from pydantic import BaseModel, Field
from typing import List, Optional

class RecipeCriteria(BaseModel):
    diet: Optional[str] = Field(None, example="vegan")
    includeIngredients: Optional[str] = Field(None, example="tomatoes, cheese")
    type: Optional[str] = Field(None, example="main course")
    intolerances: Optional[str] = Field(None, example="dairy")
    instructionsRequired: bool = Field(default=True)
    number: int = Field(default=10, ge=1, le=100)  # Assuming number must be between 1 and 100

class ProcessRecipesCriteria(BaseModel):
    criteria: List[RecipeCriteria]

class RecipeIDRequest(BaseModel):
    recipe_id: int