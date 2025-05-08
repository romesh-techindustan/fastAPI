from http.client import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.hobby

user_collection = database.get_collection("users")


async def check_db_connection():
    try:
        await client.admin.command("ping")
        print("MongoDB connected successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="MongoDB connection failed")
