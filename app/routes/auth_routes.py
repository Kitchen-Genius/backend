# app/routes/auth_routes.py

from fastapi import APIRouter, Body
from app.services.auth_service import authenticate_user

router = APIRouter()

@router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    user = await authenticate_user(email, password)
    # Here, you can generate and return a JWT or any token for session management
    return {"message": "User authenticated successfully", "user": user}
