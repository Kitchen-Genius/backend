# app/services/auth_service.py

from app.database.db import users
from fastapi import HTTPException, status
import bcrypt

async def authenticate_user(email: str, password: str):
    user = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return user  # Or True, depending on how you wish to handle successful authentication
