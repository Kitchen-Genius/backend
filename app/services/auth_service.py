# app/services/auth_service.py

from app.database.db import users
from fastapi import HTTPException, status
import bcrypt

async def authenticate_user(email: str, password: str):
    user = await users.find_one({"email": email})
    if not user:
        return False

    stored_hashed_password = user['password']
    password_bytes = password.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, stored_hashed_password):
        # Authentication successful
        return True
    else:
        # Authentication failed
        return False
