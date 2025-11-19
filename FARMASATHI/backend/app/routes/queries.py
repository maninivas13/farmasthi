# routes/queries.py - Query Management Routes

from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.query import QueryCreate, QueryResponse, QueryUpdate, OfficerReply, QueryStatus
from app.models.notification import NotificationCreate, NotificationType
from app.database import get_queries_collection, get_notifications_collection
from app.utils.security import get_current_user, require_officer_role
from datetime import datetime
from bson import ObjectId
from typing import List, Optional

router = APIRouter(prefix="/api/queries", tags=["Queries"])

@router.post("/submit", response_model=QueryResponse, status_code=status.HTTP_201_CREATED)
async def submit_query(query: QueryCreate, current_user: dict = Depends(get_current_user)):
    """Submit a new farmer query"""
    queries_collection = await get_queries_collection()
    
    # Create query document
    query_doc = {
        **query.dict(),
        "farmer_id": current_user["user_id"],
        "status": QueryStatus.OPEN,
        "created_at": datetime.utcnow(),
        "assigned_to": None,
        "officer_name": None
    }
    
    # Insert query
    result = await queries_collection.insert_one(query_doc)
    query_id = str(result.inserted_id)
    
    # Create notification for officers
    notifications_collection = await get_notifications_collection()
    notification = {
        "user_id": "all_officers",  # Broadcast to all officers
        "title": "New Query Submitted",
        "message": f"New {query.urgency} query from {query.farmer_name}",
        "notification_type": NotificationType.QUERY_SUBMITTED,
        "query_id": query_id,
        "created_at": datetime.utcnow(),
        "read": False
    }
    await notifications_collection.insert_one(notification)
    
    # Return query response
    return QueryResponse(
        id=query_id,
        **query.dict(),
        status=QueryStatus.OPEN,
        created_at=query_doc["created_at"]
    )

@router.get("/history", response_model=List[QueryResponse])
async def get_query_history(
    current_user: dict = Depends(get_current_user),
    status: Optional[QueryStatus] = None,
    limit: int = Query(50, le=100)
):
    """Get query history for current user"""
    queries_collection = await get_queries_collection()
    
    # Build query filter
    filter_query = {}
    
    if current_user["role"] == "farmer":
        filter_query["farmer_id"] = current_user["user_id"]
    elif current_user["role"] == "officer" and status:
        filter_query["status"] = status
    
    # Fetch queries
    cursor = queries_collection.find(filter_query).sort("created_at", -1).limit(limit)
    queries = await cursor.to_list(length=limit)
    
    # Convert to response model
    response_queries = []
    for query_doc in queries:
        response_queries.append(QueryResponse(
            id=str(query_doc["_id"]),
            farmer_name=query_doc["farmer_name"],
            farmer_id=query_doc["farmer_id"],
            location=query_doc.get("location"),
            crop_type=query_doc.get("crop_type"),
            query_text=query_doc["query_text"],
            category=query_doc["category"],
            urgency=query_doc["urgency"],
            image_path=query_doc.get("image_path"),
            audio_path=query_doc.get("audio_path"),
            status=query_doc["status"],
            assigned_to=query_doc.get("assigned_to"),
            officer_name=query_doc.get("officer_name"),
            created_at=query_doc["created_at"],
            updated_at=query_doc.get("updated_at"),
            ai_analysis=query_doc.get("ai_analysis"),
            reply=query_doc.get("reply")
        ))
    
    return response_queries

@router.get("/{query_id}", response_model=QueryResponse)
async def get_query_details(query_id: str, current_user: dict = Depends(get_current_user)):
    """Get detailed information about a specific query"""
    queries_collection = await get_queries_collection()
    
    try:
        query_doc = await queries_collection.find_one({"_id": ObjectId(query_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query ID"
        )
    
    if not query_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query not found"
        )
    
    # Check access permissions
    if current_user["role"] == "farmer" and query_doc["farmer_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return QueryResponse(
        id=str(query_doc["_id"]),
        **{k: v for k, v in query_doc.items() if k != "_id"}
    )

@router.post("/{query_id}/assign", response_model=QueryResponse)
async def assign_query(
    query_id: str,
    current_user: dict = Depends(require_officer_role)
):
    """Officer assigns query to themselves"""
    queries_collection = await get_queries_collection()
    
    try:
        result = await queries_collection.find_one_and_update(
            {"_id": ObjectId(query_id)},
            {
                "$set": {
                    "status": QueryStatus.ASSIGNED,
                    "assigned_to": current_user["user_id"],
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query ID"
        )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query not found"
        )
    
    # Create notification for farmer
    notifications_collection = await get_notifications_collection()
    notification = {
        "user_id": result["farmer_id"],
        "title": "Query Assigned",
        "message": "Your query has been assigned to an officer",
        "notification_type": NotificationType.QUERY_ASSIGNED,
        "query_id": query_id,
        "created_at": datetime.utcnow(),
        "read": False
    }
    await notifications_collection.insert_one(notification)
    
    return QueryResponse(
        id=str(result["_id"]),
        **{k: v for k, v in result.items() if k != "_id"}
    )

@router.post("/{query_id}/reply", response_model=QueryResponse)
async def reply_to_query(
    query_id: str,
    reply: OfficerReply,
    current_user: dict = Depends(require_officer_role)
):
    """Officer replies to a query"""
    queries_collection = await get_queries_collection()
    
    update_data = {
        "reply": reply.reply_text,
        "updated_at": datetime.utcnow()
    }
    
    if reply.mark_resolved:
        update_data["status"] = QueryStatus.RESOLVED
    
    try:
        result = await queries_collection.find_one_and_update(
            {"_id": ObjectId(query_id)},
            {"$set": update_data},
            return_document=True
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query ID"
        )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query not found"
        )
    
    # Create notification for farmer
    notifications_collection = await get_notifications_collection()
    notification = {
        "user_id": result["farmer_id"],
        "title": "Officer Replied" if not reply.mark_resolved else "Query Resolved",
        "message": "An agricultural officer has responded to your query",
        "notification_type": NotificationType.QUERY_REPLIED if not reply.mark_resolved else NotificationType.QUERY_RESOLVED,
        "query_id": query_id,
        "created_at": datetime.utcnow(),
        "read": False
    }
    await notifications_collection.insert_one(notification)
    
    return QueryResponse(
        id=str(result["_id"]),
        **{k: v for k, v in result.items() if k != "_id"}
    )

@router.get("/statistics/overview")
async def get_statistics(current_user: dict = Depends(require_officer_role)):
    """Get query statistics for dashboard"""
    queries_collection = await get_queries_collection()
    
    total = await queries_collection.count_documents({})
    open_count = await queries_collection.count_documents({"status": QueryStatus.OPEN})
    assigned = await queries_collection.count_documents({"status": QueryStatus.ASSIGNED})
    resolved = await queries_collection.count_documents({"status": QueryStatus.RESOLVED})
    urgent = await queries_collection.count_documents({"urgency": "high", "status": {"$ne": QueryStatus.RESOLVED}})
    
    return {
        "total": total,
        "open": open_count,
        "assigned": assigned,
        "resolved": resolved,
        "urgent": urgent,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 2)
    }
