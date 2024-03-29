from pydantic import BaseModel, Field
from typing import List, Optional

"""This file defines models related to recipe criteria and processing. 
These models are used to validate the data for recipe searches and processing requests."""


class RecipeCriteria(BaseModel):
    """Represents search criteria for recipes. Each attribute corresponds to a search parameter, 
    such as diet preference, ingredients, etc. Optional fields allow flexibility in search queries"""
    diet: Optional[str] = Field(None, example="vegan")
    includeIngredients: Optional[str] = Field(None, example="tomatoes, cheese")
    type: Optional[str] = Field(None, example="main course")
    intolerances: Optional[str] = Field(None, example="dairy")
    instructionsRequired: bool = Field(default=True)
    number: int = Field(default=10, ge=1, le=100)



class ProcessRecipesCriteria(BaseModel):
    """A wrapper model that holds a list of RecipeCriteria objects, 
    enabling bulk processing of multiple search criteria sets"""
    criteria: List[RecipeCriteria]



class RecipeIDRequest(BaseModel):
    """A simple model to encapsulate a recipe ID for operations 
    requiring a single recipe's identification."""
    recipe_id: int