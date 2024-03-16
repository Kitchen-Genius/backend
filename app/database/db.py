from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS")  # Load from environment variables

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.KitchenGenius

# collections:
ingredients_collection = database.Ingredients
saved_recipes = database.saved_recipes
users = database.users