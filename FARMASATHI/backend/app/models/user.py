# models/user.py - User Pydantic Models

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    FARMER = "farmer"
    OFFICER = "officer"
    ADMIN = "admin"

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: str = Field(..., pattern=r"^\d{10}$")
    role: UserRole = UserRole.FARMER

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    location: Optional[str] = None
    department: Optional[str] = None  # For officers

class UserLogin(BaseModel):
    phone: str = Field(..., pattern=r"^\d{10}$")
    password: str = Field(..., min_length=6)
    role: UserRole

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    location: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime
    is_active: bool = True
    
    class Config:
        populate_by_name = True

class UserResponse(UserBase):
    id: str
    location: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: str
    role: UserRole
