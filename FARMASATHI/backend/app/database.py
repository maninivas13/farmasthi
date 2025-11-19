# database.py - MongoDB Connection and Configuration

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "agriassist_db")

from typing import Optional

# Async MongoDB client for FastAPI
class Database:
    client: Optional[AsyncIOMotorClient] = None
    mock_users = {}  # In-memory storage when MongoDB unavailable
    mock_queries = []
    
database = Database()

async def get_database() -> Optional[AsyncIOMotorDatabase]:
    if database.client is None:
        return None
    return database.client[DATABASE_NAME]

async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    database.client = AsyncIOMotorClient(MONGODB_URL)
    print(f"✅ Connected to MongoDB at {MONGODB_URL}")
    
async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    if database.client is not None:
        database.client.close()
        print("❌ Closed MongoDB connection")
    else:
        print("⚠️  No MongoDB connection to close")

# Collections
async def get_users_collection():
    db = await get_database()
    if db is None:
        return None  # Return None if no database
    return db.users

async def get_queries_collection():
    db = await get_database()
    if db is None:
        return None
    return db.queries

async def get_responses_collection():
    db = await get_database()
    if db is None:
        return None
    return db.responses

async def get_notifications_collection():
    db = await get_database()
    if db is None:
        return None
    return db.notifications

# Initialize indexes
async def init_db():
    """Initialize database indexes"""
    try:
        db = await get_database()
        if db is None:
            print("⚠️  Running without database - skipping index initialization")
            return
        
        # Users collection indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("phone")
        
        # Queries collection indexes
        await db.queries.create_index("farmer_id")
        await db.queries.create_index("status")
        await db.queries.create_index("created_at")
        await db.queries.create_index("urgency")
        
        # Notifications collection indexes
        await db.notifications.create_index("user_id")
        await db.notifications.create_index("created_at")
        
        print("✅ Database indexes initialized")
    except Exception as e:
        print(f"⚠️  Could not initialize database indexes: {e}")
        print("⚠️  Running without database indexes")
