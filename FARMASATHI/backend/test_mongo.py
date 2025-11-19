import asyncio
from app.database import connect_to_mongo, close_mongo_connection, get_users_collection

async def test_mongo():
    try:
        print("Connecting to MongoDB...")
        await connect_to_mongo()
        print("✅ Connected successfully!")
        
        # Test collection access
        users_collection = await get_users_collection()
        if users_collection:
            print("✅ Collection access working!")
        else:
            print("❌ Collection access failed")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        try:
            await close_mongo_connection()
            print("Disconnected from MongoDB")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_mongo())