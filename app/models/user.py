from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException

app = FastAPI()


class User(BaseModel):
    email: EmailStr
    password: str  # This should be a hashed password in a real-world scenario


MONGODB_URI = "mongodb+srv://KGUser:jXH2M8loFrZjtSYR@cluster0.v1oaihv.mongodb.net/"
DATABASE_NAME = "KitchenGenius"
COLLECTION_NAME = "users"

# Create a MongoClient instance
client = MongoClient(MONGODB_URI)

# Connect to the specified database and collection
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


@app.post("/check_user_credentials")
async def check_user_credentials(user: User):
    try:
        # Query the "users" collection to find a matching user
        result = collection.find_one({"email": user.email, "password": user.password})

        # If user is found, return True; otherwise, return False
        return {"result": True} if result else {"result": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
