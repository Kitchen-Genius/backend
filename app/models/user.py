# app/models/user.py

from pydantic import BaseModel, EmailStr, Field

"""Defines models related to user information and authentication"""


class User(BaseModel):
    """A basic model for representing a user, including their email and (hashed) password. 
    Important for authentication processes"""
    email: EmailStr
    password: str  # This should be a hashed password



class UserSignUpRequest(BaseModel):
    """Extends the User model with additional fields for the signup process, 
    including the user's name and an image link. 
    This model is used to validate signup requests"""
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="strongpassword")
    img_link: str = Field(..., example="https://example.com/image.jpg")