# app/routes/auth_routes.py

from fastapi import APIRouter, Body, HTTPException
from app.services.auth_service import authenticate_user, get_user_by_email, create_user
from fastapi.encoders import jsonable_encoder
from app.utils.serialize_doc import serialize_document
from app.models.user import UserSignUpRequest



router = APIRouter()

@router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    authenticated = await authenticate_user(email, password)
    if not authenticated:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    # Assuming get_user_by_email is a function that fetches the user document by email
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    serialized_data = serialize_document(user)
    # Here, you can generate and return a JWT or any token for session management
    return jsonable_encoder(serialized_data)

@router.post("/signup")
async def signup(user_data: UserSignUpRequest):
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    return await create_user(user_data)