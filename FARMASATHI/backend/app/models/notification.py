# models/notification.py - Notification Pydantic Models

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    QUERY_SUBMITTED = "query_submitted"
    QUERY_ASSIGNED = "query_assigned"
    QUERY_REPLIED = "query_replied"
    QUERY_RESOLVED = "query_resolved"
    SYSTEM = "system"

class NotificationBase(BaseModel):
    user_id: str
    title: str
    message: str
    notification_type: NotificationType
    query_id: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationInDB(NotificationBase):
    id: str = Field(alias="_id")
    created_at: datetime
    read: bool = False
    
    class Config:
        populate_by_name = True

class NotificationResponse(NotificationBase):
    id: str
    created_at: datetime
    read: bool
