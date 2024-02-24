from fastapi import APIRouter, Depends, Body, HTTPException
from app.services import spoonacular as spoonacular_service
from app.services.recipe_processing import process_and_save_recipes, prepare_recipe_search_criteria
from app.utils.validations import validate_diet, validate_type, validate_intolerances
from app.models.recipe_models import ProcessRecipesCriteria

router = APIRouter()

@router.get("/search-recipes/")
async def search_recipes(
    diet: str = Depends(validate_diet),
    includeIngredients: str = None, 
    type: str = Depends(validate_type), 
    intolerances: str = Depends(validate_intolerances), 
    instructionsRequired: bool = True, 
    number: int = 1
):
    data = await spoonacular_service.search_recipes(diet, includeIngredients, type, intolerances, instructionsRequired, number)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    return data

@router.get("/processed-recipes/")
async def get_processed_recipes(
    diet: str = Depends(validate_diet), 
    includeIngredients: str = None, 
    type: str = Depends(validate_type), 
    intolerances: str = Depends(validate_intolerances)
):
    processed_recipes = await spoonacular_service(diet, includeIngredients, type, intolerances)
    if "error" in processed_recipes:
        raise HTTPException(status_code=400, detail=processed_recipes["error"])
    return processed_recipes

@router.get("/recipes/")
async def get_recipes(
    diet: str = Depends(validate_diet),
    includeIngredients: str = None,
    type: str = Depends(validate_type),
    intolerances: str = Depends(validate_intolerances),
    instructionsRequired: bool = True,
    number: int = 1
):
    try:
        recipes = await spoonacular_service.search_recipes(diet=diet, includeIngredients=includeIngredients, type=type, intolerances=intolerances, instructionsRequired=instructionsRequired, number=number)
        return recipes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/processed-recipes/")
async def get_processed_recipes(
    diet: str = Depends(validate_diet),
    includeIngredients: str = None,
    type: str = Depends(validate_type),
    intolerances: str = Depends(validate_intolerances),
    instructionsRequired: bool = True,
    number: int = 1
):
    try:
        processed_recipes = await process_and_save_recipes(diet=diet, includeIngredients=includeIngredients, type=type, intolerances=intolerances, instructionsRequired=instructionsRequired, number=number)
        return processed_recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/process-recipes-criteria")
async def process_recipes_criteria(criteria: ProcessRecipesCriteria = Body(...)):
    try:
        processed_recipes_list = []
        for criteria_set in criteria.criteria:
            criteria_dict = criteria_set.model_dump()
            search_criteria = prepare_recipe_search_criteria([criteria_dict])  # Adjust if your logic expects a list
            processed_recipes = await process_and_save_recipes(
                diet=search_criteria["diet"],
                includeIngredients=search_criteria["includeIngredients"],
                type=criteria_dict.get("type", ""),
                intolerances=criteria_dict.get("intolerances", ""),
                instructionsRequired=criteria_dict.get("instructionsRequired", True),
                number=criteria_dict.get("number", 10)
            )
            processed_recipes_list.append(processed_recipes)
        
        return processed_recipes_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))