# app/services/auth_service.py

from app.database.db import users
from fastapi import HTTPException, status
import bcrypt

async def authenticate_user(email: str, password: str):
    user = await users.find_one({"email": email})
    if not user:
        return False

    password_bytes = password.encode('utf-8')
    hashed_password_bytes = user['password'].encode('utf-8')

    if bcrypt.checkpw(password_bytes, hashed_password_bytes):
        return True
    else:
        return False
