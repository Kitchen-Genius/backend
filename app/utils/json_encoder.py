# /app/utils/json_encoder.py

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder class to convert ObjectId to str."""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def custom_json_response(content: dict):
    """Generates a JSONResponse using the custom JSON encoder."""
    content_json = json.loads(json.dumps(content, cls=JSONEncoder))  # Serialize with custom encoder
    return JSONResponse(content=jsonable_encoder(content_json))