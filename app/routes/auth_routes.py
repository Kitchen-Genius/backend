# app/routes/auth_routes.py

from fastapi import APIRouter, Body
from app.services.auth_service import authenticate_user
from fastapi.encoders import jsonable_encoder
from app.utils.serialize_doc import serialize_document


router = APIRouter()

@router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    user = await authenticate_user(email, password)
    serialized_data = serialize_document(user)
    # Here, you can generate and return a JWT or any token for session management
    return jsonable_encoder(serialized_data)
