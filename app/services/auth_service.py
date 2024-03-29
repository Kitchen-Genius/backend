# app/services/auth_service.py

from bson import Binary
from app.database.db import users, database
from passlib.context import CryptContext
from app.models.user import UserSignUpRequest
import bcrypt

"""Handles authentication logic, user creation, and user retrieval"""

async def authenticate_user(email: str, password: str):
    """Validates user credentials against stored data"""
    user = await users.find_one({"email": email})
    if not user:
        return False

    stored_hashed_password = user['password']
    password_bytes = password.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, stored_hashed_password):
        # Authentication successful
        return user
    else:
        # Authentication failed
        return None

async def get_user_by_email(email: str):
    """Retrieves a user document from the database by email"""
    user_doc = await users.find_one({"email": email})
    return user_doc  # You might want to serialize this document before returning

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user_data: UserSignUpRequest):
    """Registers a new user, ensuring unique email addresses, hashing passwords, and assigning a new user_id"""
    # Check if the user already exists
    existing_user = await database.users.find_one({"email": user_data.email})
    if existing_user:
        return {"message": "User already exists", "status_code": 400}

    # Generate the new user_id by incrementing the largest existing user_id
    max_user_doc = await database.users.find_one(sort=[("user_id", -1)])
    new_user_id = 1 if max_user_doc is None else max_user_doc["user_id"] + 1

    # Hash the password
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    # Convert the hashed password to the binary format to match existing passwords
    binary_hashed_password = Binary(hashed_password)

    # Create the user document with an empty favorites list and hashed password
    user_document = {
        "user_id": new_user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": binary_hashed_password,
        "img_link": user_data.img_link,
        "favorites": []
    }
    
    await database.users.insert_one(user_document)

    return {"message": "User created successfully", "user_id": new_user_id, "status_code": 200}
