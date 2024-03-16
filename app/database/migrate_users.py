# /app/database/migrate_users.py
from dotenv import load_dotenv
load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient
import os

print("Migrate users script started")

MONGO_DETAILS = os.getenv("MONGO_DETAILS")
print(f"After loading .env, MONGO_DETAILS: {MONGO_DETAILS}")

async def migrate_user_documents():
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client.KitchenGenius
    users = database.users

    count = await users.count_documents({})
    print(f"Total users in database: {count}")

    async for user in users.find():
        print(f"Starting migration for user {user.get('email')}")
        new_structure = {
            "user_id": user.get("user_id", 0),
            "name": user.get("username", ""),
            "email": user.get("email", ""),
            "password": user.get("password", ""),
            "img_link": user.get("img", ""),
            "favorites": []  # Assuming you'll populate this later
        }
        await users.replace_one({"_id": user["_id"]}, new_structure)
        print(f"Updated user {user.get('email')} to new structure")

    print("Migration completed.")
    
def run_migration():
    import asyncio
    loop = asyncio.get_event_loop()  # Get the event loop for the current context
    loop.run_until_complete(migrate_user_documents())  # Run the async migration function

if __name__ == "__main__":
    run_migration()