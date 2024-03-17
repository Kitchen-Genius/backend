# app/models/user.py

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    password: str  # This should be a hashed password

class UserSignUpRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="strongpassword")
    img_link: str = Field(..., example="https://example.com/image.jpg")