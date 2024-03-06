#!/usr/bin/env python3

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import bcrypt
from urllib.parse import quote_plus


# Load the environment variables
load_dotenv()

# Prepare the MongoDB connection details
username = quote_plus("KGUser")
password = quote_plus("ybEbYAmVImLUvSBp")
cluster_url = "cluster0.v1oaihv.mongodb.net/KitchenGenius.users?retryWrites=true&w=majority"

# Connect to MongoDB
MONGO_DETAILS = f"mongodb+srv://{username}:{password}@{cluster_url}"
client = MongoClient(MONGO_DETAILS, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.KitchenGenius 
users_collection = db.users 

# List of users to insert
users = [
    "almog@gmail.com",
    "kitchen@genius.com",
    "regev@gmail.com",
    "esty@gmail.com"
]

# Hash the password
password = "123"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Insert users
for user_email in users:
    user_document = {
        "email": user_email,
        "password": hashed_password,
        # Add any other fields you need for your user document
    }
    # Insert the user into the collection, if it doesn't already exist
    if not users_collection.find_one({"email": user_email}):
        users_collection.insert_one(user_document)
        print(f"User {user_email} added.")
    else:
        print(f"User {user_email} already exists.")

print("Users insertion completed.")
