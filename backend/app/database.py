from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import asyncio

client: AsyncIOMotorClient = None
db = None

async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        await client.admin.command('ping')
        db = client[settings.MONGODB_DATABASE]
        # Create indexes
        await db.analyses.create_index("createdAt")
        await db.analyses.create_index("analysisId", unique=True)
        await db.comment_predictions.create_index("analysisId")
        await db.comment_predictions.create_index("sentiment")
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("   App will run without database. History/storage disabled.")
        db = None
        client = None

async def close_db():
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed")

def get_db():
    return db
