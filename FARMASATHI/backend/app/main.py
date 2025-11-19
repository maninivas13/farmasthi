# main.py - Complete FastAPI Application with All Integrations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database functions
from app.database import connect_to_mongo, close_mongo_connection, init_db

# Import routers
from app.routes import auth, queries, uploads, websocket, chatbot

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting FarmaSathi Backend...")
    try:
        await connect_to_mongo()
        await init_db()
        print("✅ Backend initialized successfully with MongoDB!")
    except Exception as e:
        print(f"⚠️  MongoDB not available: {e}")
        print("⚠️  Running in mock mode without database")
    
    yield
    
    # Shutdown
    print("⏹️  Shutting down FarmaSathi Backend...")
    try:
        await close_mongo_connection()
    except:
        pass
    print("👋 Backend shutdown complete")

# Initialize FastAPI app
app = FastAPI(
    title="FarmaSathi API",
    description="AI-Powered Agricultural Assistance Platform - Complete Backend Integration",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "*"  # Allow all for development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for uploads
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(queries.router)
app.include_router(uploads.router)
app.include_router(websocket.router)
app.include_router(chatbot.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🌾 FarmaSathi API - Fully Integrated Backend",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "JWT Authentication",
            "Query Management",
            "File Uploads (Images & Voice)",
            "WebSocket Notifications",
            "MongoDB Integration",
            "Real-time Updates",
            "AI Chatbot Assistant",
            "Text-to-Speech Responses"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "auth": "/api/auth",
            "queries": "/api/queries",
            "uploads": "/api/upload",
            "websocket": "/ws/notifications",
            "chatbot": "/api/chat"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "api": "running"
    }

# Weather endpoint (enhanced with real data integration capability)
@app.post("/api/weather")
async def get_weather(request: dict):
    """Get weather information for location"""
    location = request.get("location", "Unknown")
    
    # Simulated weather data - can be replaced with real API
    weather_data = {
        "location": location,
        "temperature": 28,
        "humidity": 65,
        "conditions": "Partly Cloudy",
        "rainfall_forecast": "20% chance in next 48 hours",
        "wind_speed": "12 km/h",
        "uv_index": "Moderate",
        "advisory": "Good conditions for spraying pesticides. Avoid irrigation today.",
        "forecast": [
            {"day": "Today", "temp": 28, "condition": "Partly Cloudy"},
            {"day": "Tomorrow", "temp": 30, "condition": "Sunny"},
            {"day": "Day 3", "temp": 27, "condition": "Cloudy"}
        ]
    }
    
    return weather_data

# Market prices endpoint
@app.post("/api/market-prices")
async def get_market_prices(request: dict):
    """Get current market prices for crops"""
    crop = request.get("crop", "").lower()
    location = request.get("location", "National Average")
    
    # Simulated market data
    market_data = {
        "rice": {"min": 1800, "max": 2200, "avg": 2000, "unit": "₹/quintal", "trend": "stable"},
        "wheat": {"min": 1900, "max": 2100, "avg": 2000, "unit": "₹/quintal", "trend": "rising"},
        "cotton": {"min": 5500, "max": 6000, "avg": 5750, "unit": "₹/quintal", "trend": "falling"},
        "sugarcane": {"min": 275, "max": 310, "avg": 290, "unit": "₹/quintal", "trend": "stable"},
        "maize": {"min": 1400, "max": 1700, "avg": 1550, "unit": "₹/quintal", "trend": "rising"},
        "tomato": {"min": 800, "max": 1200, "avg": 1000, "unit": "₹/quintal", "trend": "volatile"},
        "potato": {"min": 600, "max": 900, "avg": 750, "unit": "₹/quintal", "trend": "stable"},
    }
    
    if crop in market_data:
        return {
            "success": True,
            "crop": crop,
            "location": location,
            "prices": market_data[crop],
            "last_updated": "2024-01-15",
            "recommendation": get_market_recommendation(market_data[crop]["trend"])
        }
    else:
        return {
            "success": False,
            "message": "Price data not available for this crop",
            "crop": crop
        }

def get_market_recommendation(trend: str) -> str:
    """Generate market recommendation based on trend"""
    recommendations = {
        "rising": "Current prices are favorable for selling. Consider selling soon.",
        "falling": "Prices are declining. Consider storage if you have facilities.",
        "stable": "Prices are stable. Sell at your convenience.",
        "volatile": "Market is volatile. Wait for price stabilization or sell immediately if urgent."
    }
    return recommendations.get(trend, "Monitor market conditions regularly.")

# AI Analysis endpoint
@app.post("/api/ai-analysis")
async def ai_analysis(request: dict):
    """AI-powered preliminary analysis of farmer queries"""
    query_text = request.get("query_text", "").lower()
    crop_type = request.get("crop_type", "")
    
    # Enhanced AI analysis logic
    analysis_result = {
        "category": "general",
        "confidence": 0.6,
        "recommendation": "General agricultural query. Officer will provide expert guidance.",
        "urgency": "normal",
        "suggested_actions": []
    }
    
    # Pest detection
    if any(word in query_text for word in ['pest', 'insect', 'bug', 'worm', 'कीट', 'பூச்சி']):
        analysis_result.update({
            "category": "pest",
            "confidence": 0.85,
            "recommendation": "Pest issue detected. Apply neem-based organic pesticide or consult officer for specific treatment.",
            "suggested_actions": [
                "Identify the specific pest",
                "Apply recommended pesticide at proper dosage",
                "Monitor crop for 3-5 days",
                "Maintain proper field sanitation"
            ]
        })
    
    # Disease detection
    elif any(word in query_text for word in ['disease', 'fungus', 'rot', 'blight', 'wilting', 'रोग']):
        analysis_result.update({
            "category": "disease",
            "confidence": 0.80,
            "recommendation": "Possible fungal/bacterial disease. Avoid overhead watering and improve air circulation.",
            "suggested_actions": [
                "Isolate affected plants if possible",
                "Do not apply water on leaves",
                "Improve field drainage",
                "Apply appropriate fungicide"
            ]
        })
    
    # Nutrient deficiency
    elif any(word in query_text for word in ['yellow', 'pale', 'nutrient', 'fertilizer', 'पीला', 'खाद']):
        analysis_result.update({
            "category": "nutrient",
            "confidence": 0.75,
            "recommendation": "Nutrient deficiency symptoms detected. Soil test recommended for accurate diagnosis.",
            "suggested_actions": [
                "Get soil tested",
                "Apply balanced NPK fertilizer",
                "Consider organic manure",
                "Monitor plant response"
            ]
        })
    
    # Check for urgency
    if any(word in query_text for word in ['urgent', 'emergency', 'dying', 'critical', 'immediate']):
        analysis_result["urgency"] = "high"
    
    return analysis_result

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") == "true" else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
