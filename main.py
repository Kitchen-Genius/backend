# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.recipe_routes import router as recipe_router
from app.routes import auth_routes
from dotenv import load_dotenv
import os

# from app.database.db import client

load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

app = FastAPI()

app.include_router(recipe_router)
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

# List of origins allowed to make requests to this API
origins = [
    "http://localhost:3000",  # React's default development port
    "https://frontend-nu-murex.vercel.app",  # Adjust for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(ingredients_router)

# @app.on_event("startup")
# async def startup_event():
    # Example: Connect to the database (if needed)
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
    # Example: Close database connection (if needed)
#     await client.close()
