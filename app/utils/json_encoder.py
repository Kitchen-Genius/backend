# /app/utils/json_encoder.py

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from bson import ObjectId

"""Provides custom JSON encoding functionality to handle MongoDB-specific data types 
(e.g., ObjectId) which are not natively serializable by Python's standard JSON encoder"""

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder class to convert ObjectId to str."""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def custom_json_response(content: dict):
    """
    Generates a custom JSONResponse for content that includes MongoDB ObjectId fields.
    Utilizes a custom JSON encoder to convert ObjectId instances to strings.
    This function ensures API responses can serialize MongoDB documents directly.

    Parameters:
    - content (dict): The content to be serialized and included in the JSONResponse.

    Returns:
    - JSONResponse: A FastAPI JSONResponse object with content serialized using the custom encoder.
    """
    content_json = json.loads(json.dumps(content, cls=JSONEncoder))  # Serialize with custom encoder
    return JSONResponse(content=jsonable_encoder(content_json))