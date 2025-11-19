from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="FarmaSathi API",
    description="AI-Powered Agricultural Assistance Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# PYDANTIC MODELS
# ========================================

class QuerySubmission(BaseModel):
    farmer_name: str
    location: Optional[str] = None
    crop_type: Optional[str] = None
    query_text: str
    urgency: Optional[str] = "normal"
    category: Optional[str] = "general"
    has_image: Optional[bool] = False
    has_audio: Optional[bool] = False

class QueryResponse(BaseModel):
    query_id: int
    officer_name: str
    response_text: str
    status: str

class WeatherRequest(BaseModel):
    location: str

class MarketPriceRequest(BaseModel):
    crop: str
    location: Optional[str] = None

class AIAnalysisRequest(BaseModel):
    query_text: str
    crop_type: Optional[str] = None
    has_image: Optional[bool] = False

# ========================================
# ROOT ENDPOINT
# ========================================

@app.get("/")
def root():
    return {
        "message": "FarmaSathi API Running Successfully ✅",
        "version": "1.0.0",
        "status": "active",
        "endpoints": [
            "/queries",
            "/weather",
            "/market-prices",
            "/ai-analysis"
        ]
    }

# ========================================
# QUERY MANAGEMENT ENDPOINTS
# ========================================

@app.post("/api/queries")
def submit_query(query: QuerySubmission):
    """Submit a new farmer query"""
    try:
        query_id = int(datetime.now().timestamp() * 1000)
        
        return {
            "success": True,
            "query_id": query_id,
            "message": "Query submitted successfully",
            "estimated_response_time": "24 hours",
            "status": "open"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/queries/{query_id}")
def get_query(query_id: int):
    """Get query details by ID"""
    return {
        "query_id": query_id,
        "status": "open",
        "message": "Query retrieved successfully"
    }

@app.post("/api/queries/{query_id}/respond")
def respond_to_query(query_id: int, response: QueryResponse):
    """Officer responds to a query"""
    return {
        "success": True,
        "query_id": query_id,
        "message": "Response submitted successfully",
        "status": "resolved"
    }

# ========================================
# AI ANALYSIS ENDPOINT
# ========================================

@app.post("/api/ai-analysis")
def ai_analysis(request: AIAnalysisRequest):
    """AI-powered preliminary analysis of farmer queries"""
    query_text = request.query_text.lower()
    
    # Pest detection
    if any(word in query_text for word in ['pest', 'insect', 'bug', 'worm']):
        category = "pest"
        confidence = 0.85
        recommendation = "Appears to be a pest issue. Apply neem-based organic pesticide or consult officer."
    
    # Disease detection
    elif any(word in query_text for word in ['disease', 'fungus', 'rot', 'blight', 'wilting']):
        category = "disease"
        confidence = 0.80
        recommendation = "Possible fungal/bacterial disease. Avoid overhead watering. Expert diagnosis recommended."
    
    # Nutrient deficiency
    elif any(word in query_text for word in ['yellow', 'pale', 'nutrient', 'fertilizer']):
        category = "nutrient"
        confidence = 0.75
        recommendation = "Nutrient deficiency detected. Apply balanced NPK fertilizer. Soil test recommended."
    
    # Weather related
    elif any(word in query_text for word in ['weather', 'rain', 'drought', 'flood']):
        category = "weather"
        confidence = 0.70
        recommendation = "Weather-related concern. Monitor forecasts and ensure proper drainage."
    
    # Market related
    elif any(word in query_text for word in ['market', 'price', 'sell', 'storage']):
        category = "market"
        confidence = 0.75
        recommendation = "Market query. Check local mandi prices. Our analyst will provide strategy."
    
    else:
        category = "general"
        confidence = 0.60
        recommendation = "General agricultural query. Officer will provide expert guidance within 24 hours."
    
    return {
        "category": category,
        "confidence": confidence,
        "recommendation": recommendation,
        "urgency": "high" if any(word in query_text for word in ['urgent', 'emergency', 'dying']) else "normal"
    }

# ========================================
# WEATHER ENDPOINT
# ========================================

@app.post("/api/weather")
def get_weather(request: WeatherRequest):
    """Get weather information for a location"""
    # Simulated weather data
    weather_data = {
        "location": request.location,
        "temperature": 28,
        "humidity": 65,
        "conditions": "Partly Cloudy",
        "rainfall_forecast": "20% chance in next 48 hours",
        "wind_speed": "12 km/h",
        "advisory": "Good conditions for spraying pesticides. Avoid irrigation today."
    }
    
    return weather_data

# ========================================
# MARKET PRICES ENDPOINT
# ========================================

@app.post("/api/market-prices")
def get_market_prices(request: MarketPriceRequest):
    """Get current market prices for crops"""
    
    # Simulated market data
    market_data = {
        "rice": {"min": 1800, "max": 2200, "avg": 2000, "unit": "₹/quintal", "trend": "stable"},
        "wheat": {"min": 1900, "max": 2100, "avg": 2000, "unit": "₹/quintal", "trend": "rising"},
        "cotton": {"min": 5500, "max": 6000, "avg": 5750, "unit": "₹/quintal", "trend": "falling"},
        "sugarcane": {"min": 275, "max": 310, "avg": 290, "unit": "₹/quintal", "trend": "stable"},
        "maize": {"min": 1400, "max": 1700, "avg": 1550, "unit": "₹/quintal", "trend": "rising"},
    }
    
    crop = request.crop.lower()
    
    if crop in market_data:
        return {
            "crop": crop,
            "location": request.location or "National Average",
            "prices": market_data[crop],
            "last_updated": datetime.now().isoformat(),
            "recommendation": "Current prices are favorable for selling" if market_data[crop]["trend"] == "rising" else "Consider storage if prices are low"
        }
    else:
        return {
            "crop": crop,
            "location": request.location or "National Average",
            "prices": {"min": 0, "max": 0, "avg": 0, "unit": "₹/quintal", "trend": "unknown"},
            "message": "Price data not available for this crop"
        }

# ========================================
# STATISTICS ENDPOINT
# ========================================

@app.get("/api/statistics")
def get_statistics():
    """Get platform statistics"""
    return {
        "total_queries": 1247,
        "resolved_queries": 982,
        "active_farmers": 3456,
        "active_officers": 45,
        "average_response_time": "18 hours",
        "satisfaction_rate": "94%"
    }

# ========================================
# HEALTH CHECK
# ========================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }