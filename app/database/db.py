from motor.motor_asyncio import AsyncIOMotorClient
import os

"""Establishes a connection to MongoDB using environment variables for configuration. 
It defines global access points for different collections within the database"""

MONGO_DETAILS = os.getenv("MONGO_DETAILS")  # Load from environment variables

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.KitchenGenius

# collections:
ingredients_collection = database.Ingredients
saved_recipes = database.saved_recipes
users = database.users