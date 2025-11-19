# routes/auth.py - Authentication Routes

from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate, UserLogin, Token, UserResponse, UserRole
from app.database import get_users_collection, database
from app.utils.security import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """Register a new user (farmer or officer)"""
    users_collection = await get_users_collection()
    
    # If no database, use mock mode
    if users_collection is None:
        # Check if user already exists in mock storage
        for mock_user in database.mock_users.values():
            if mock_user.get("phone") == user.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Create user document
        user_id = str(len(database.mock_users) + 1)
        user_doc = {
            "_id": user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "hashed_password": hashed_password,
            "location": user.location,
            "department": user.department,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Store in mock storage
        database.mock_users[user_id] = user_doc
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "role": user.role}
        )
        
        # Return token and user info
        user_response = UserResponse(
            id=user_id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            role=user.role,
            location=user.location,
            department=user.department,
            created_at=user_doc["created_at"]
        )
        
        return Token(access_token=access_token, user=user_response)
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"phone": user.phone})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user document
    user_doc = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "hashed_password": hashed_password,
        "location": user.location,
        "department": user.department,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    # Insert into database
    result = await users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_id, "role": user.role}
    )
    
    # Return token and user info
    user_response = UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        location=user.location,
        department=user.department,
        created_at=user_doc["created_at"]
    )
    
    return Token(access_token=access_token, user=user_response)

@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin):
    """Login user with phone and password"""
    users_collection = await get_users_collection()
    
    # If no database, use mock mode
    if users_collection is None:
        # Find user in mock storage
        user_doc = None
        for mock_user in database.mock_users.values():
            if mock_user.get("phone") == credentials.phone:
                user_doc = mock_user
                break
        
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(credentials.password, user_doc["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify role matches
        if user_doc["role"] != credentials.role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid role for this account"
            )
        
        # Check if account is active
        if not user_doc.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        
        user_id = str(user_doc["_id"])
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "role": user_doc["role"]}
        )
        
        # Return token and user info
        user_response = UserResponse(
            id=user_id,
            name=user_doc["name"],
            email=user_doc.get("email"),
            phone=user_doc["phone"],
            role=user_doc["role"],
            location=user_doc.get("location"),
            department=user_doc.get("department"),
            created_at=user_doc["created_at"]
        )
        
        return Token(access_token=access_token, user=user_response)
    
    # Find user by phone
    user_doc = await users_collection.find_one({"phone": credentials.phone})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(credentials.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify role matches
    if user_doc["role"] != credentials.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid role for this account"
        )
    
    # Check if account is active
    if not user_doc.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    user_id = str(user_doc["_id"])
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_id, "role": user_doc["role"]}
    )
    
    # Return token and user info
    user_response = UserResponse(
        id=user_id,
        name=user_doc["name"],
        email=user_doc.get("email"),
        phone=user_doc["phone"],
        role=user_doc["role"],
        location=user_doc.get("location"),
        department=user_doc.get("department"),
        created_at=user_doc["created_at"]
    )
    
    return Token(access_token=access_token, user=user_response)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    users_collection = await get_users_collection()
    
    # If no database, use mock mode
    if users_collection is None:
        # Find user in mock storage
        user_doc = database.mock_users.get(current_user["user_id"])
        
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user_doc["_id"]),
            name=user_doc["name"],
            email=user_doc.get("email"),
            phone=user_doc["phone"],
            role=user_doc["role"],
            location=user_doc.get("location"),
            department=user_doc.get("department"),
            created_at=user_doc["created_at"]
        )
    
    user_doc = await users_collection.find_one({"_id": ObjectId(current_user["user_id"])})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user_doc["_id"]),
        name=user_doc["name"],
        email=user_doc.get("email"),
        phone=user_doc["phone"],
        role=user_doc["role"],
        location=user_doc.get("location"),
        department=user_doc.get("department"),
        created_at=user_doc["created_at"]
    )
