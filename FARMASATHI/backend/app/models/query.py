# models/query.py - Query Pydantic Models

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class QueryStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    CLOSED = "closed"

class QueryUrgency(str, Enum):
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class QueryCategory(str, Enum):
    PEST = "pest"
    DISEASE = "disease"
    NUTRIENT = "nutrient"
    WEATHER = "weather"
    MARKET = "market"
    GENERAL = "general"

class QueryBase(BaseModel):
    farmer_name: str
    farmer_id: str
    location: Optional[str] = None
    crop_type: Optional[str] = None
    query_text: str = Field(..., min_length=10)
    category: QueryCategory = QueryCategory.GENERAL
    urgency: QueryUrgency = QueryUrgency.NORMAL

class QueryCreate(QueryBase):
    image_path: Optional[str] = None
    audio_path: Optional[str] = None

class QueryInDB(QueryBase):
    id: str = Field(alias="_id")
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: QueryStatus = QueryStatus.OPEN
    assigned_to: Optional[str] = None
    officer_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    ai_analysis: Optional[str] = None
    
    class Config:
        populate_by_name = True

class QueryResponse(QueryBase):
    id: str
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: QueryStatus
    assigned_to: Optional[str] = None
    officer_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    ai_analysis: Optional[str] = None
    reply: Optional[str] = None

class QueryUpdate(BaseModel):
    status: Optional[QueryStatus] = None
    assigned_to: Optional[str] = None
    officer_name: Optional[str] = None

class OfficerReply(BaseModel):
    query_id: str
    reply_text: str = Field(..., min_length=20)
    mark_resolved: bool = False
