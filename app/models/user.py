# app/models/user.py

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    password: str  # This should be a hashed password
