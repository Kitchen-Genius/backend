import json
from fastapi import HTTPException

def validate_params(category: str, value: str, filename: str) -> str:
    if not value:  # If the parameter is optional and not provided, skip validation
        return value
    try:
        with open(f'app/data/{filename}.json') as file:
            data = json.load(file)
        if value in data[category]:
            return value
        else:
            raise ValueError("Invalid value")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{value} is an invalid {category}")
    
def validate_diet(diet: str = None):
    if diet and not validate_params('diets', diet, 'diets'):
        raise HTTPException(status_code=400, detail=f"Invalid diet: {diet}")
    return diet

def validate_type(type: str = None):
    if type and not validate_params('meal_types', type, 'meal_types'):
        raise HTTPException(status_code=400, detail=f"Invalid type: {type}")
    return type

def validate_intolerances(intolerances: str = None):
    if intolerances and not validate_params('intolerances', intolerances, 'intolerances'):
        raise HTTPException(status_code=400, detail=f"Invalid intolerances: {intolerances}")
    return intolerances