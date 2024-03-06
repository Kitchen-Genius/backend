# /app/utils/serialize_doc.py


def serialize_document(doc):
    """Convert MongoDB document to a JSON serializable Python dict."""
    if doc is None:
        return None  # or return {} based on your preference for non-found documents
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    # Convert other non-serializable types here
    return doc