import json
from fastapi import HTTPException

"""Defines functions for validating query parameters against predefined sets of 
valid values stored in JSON files. This ensures that API endpoints receive valid data"""

def validate_params(category: str, value: str, filename: str) -> str:
    """Validates a given value against a list of allowed values for a specific category, 
    read from a JSON file. If the value is invalid, it raises an HTTPException"""
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
    """Specific validation function for recipe search parameter - diet.
    utilize 'validate_params' to check if the provided value is valid according to data stored in JSON files."""
    if diet and not validate_params('diets', diet, 'diets'):
        raise HTTPException(status_code=400, detail=f"Invalid diet: {diet}")
    return diet

def validate_type(type: str = None):
    """Specific validation function for recipe search parameter - type.
    utilize 'validate_params' to check if the provided value is valid according to data stored in JSON files."""
    if type and not validate_params('meal_types', type, 'meal_types'):
        raise HTTPException(status_code=400, detail=f"Invalid type: {type}")
    return type

def validate_intolerances(intolerances: str = None):
    """Specific validation function for recipe search parameter - intolerances.
    utilize 'validate_params' to check if the provided value is valid according to data stored in JSON files."""
    if intolerances and not validate_params('intolerances', intolerances, 'intolerances'):
        raise HTTPException(status_code=400, detail=f"Invalid intolerances: {intolerances}")
    return intolerances