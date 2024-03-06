# /app/utils/serialize_doc.py


def serialize_document(doc):
    """Convert MongoDB document to a JSON serializable Python dict."""
    if doc is None:
        return None  # or return {} based on your preference for non-found documents
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    # Convert other non-serializable types here
    return doc

def serialize_recipe_document(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    
    # Process analyzedInstructions and ingredients to ensure they are in a serializable format
    if "analyzedInstructions" in doc and isinstance(doc["analyzedInstructions"], list):
        for instruction_set in doc["analyzedInstructions"]:
            if "steps" in instruction_set:
                instruction_set["steps"] = [
                    {
                        "step": step["step"],
                        "number": step.get("number", "")
                    } for step in instruction_set["steps"]
                ]
                
    if "ingredients" in doc and isinstance(doc["ingredients"], list):
        doc["ingredients"] = [
            {
                "name": ingredient["name"],
                "image": ingredient.get("image", ""),
                "amount": {
                    "value": ingredient["amount"].get("value", ""),
                    "unit": ingredient["amount"].get("unit", "")
                }
            } for ingredient in doc["ingredients"]
        ]
    
    return doc
