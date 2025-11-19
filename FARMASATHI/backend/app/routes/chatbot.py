# chatbot.py - AI Chatbot API Routes

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

from app.utils.security import get_current_user
from app.database import get_database
from app.services.ai_assistant import ai_assistant
from app.services.tts_service import tts_service

router = APIRouter(prefix="/api/chat", tags=["AI Chatbot"])


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en", pattern="^(en|hi|te|ta|bn|mr)$")
    context: Optional[Dict] = None
    include_audio: bool = True


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    audio_url: Optional[str] = None
    data: Optional[Dict] = None
    type: str
    timestamp: str


class ChatHistory(BaseModel):
    """Chat history item"""
    id: str
    user_message: str
    bot_response: str
    audio_url: Optional[str]
    language: str
    timestamp: str


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send message to AI chatbot and get intelligent response
    
    - Handles weather queries
    - Handles market price queries
    - Handles general agricultural questions
    - Returns text and audio response
    """
    try:
        user_id = current_user["user_id"]
        
        # Get AI response
        ai_response = await ai_assistant.get_response(
            question=request.message,
            language=request.language,
            context=request.context
        )
        
        response_text = ai_response.get("text", "")
        response_data = ai_response.get("data")
        response_type = ai_response.get("type", "general")
        
        # Generate audio if requested
        audio_url = None
        if request.include_audio and response_text:
            audio_url = await tts_service.text_to_speech(
                text=response_text,
                language=request.language
            )
        
        # Save to chat history
        db = await get_database()
        chat_history = {
            "user_id": user_id,
            "user_message": request.message,
            "bot_response": response_text,
            "audio_url": audio_url,
            "language": request.language,
            "response_type": response_type,
            "data": response_data,
            "timestamp": datetime.utcnow()
        }
        await db.chat_history.insert_one(chat_history)
        
        return ChatResponse(
            message=response_text,
            audio_url=audio_url,
            data=response_data,
            type=response_type,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        print(f"❌ Chat Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/history", response_model=List[ChatHistory])
async def get_chat_history(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's chat history with AI assistant
    """
    try:
        user_id = current_user["user_id"]
        db = await get_database()
        
        # Fetch chat history
        cursor = db.chat_history.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)
        
        history = []
        async for chat in cursor:
            history.append(ChatHistory(
                id=str(chat["_id"]),
                user_message=chat["user_message"],
                bot_response=chat["bot_response"],
                audio_url=chat.get("audio_url"),
                language=chat["language"],
                timestamp=chat["timestamp"].isoformat()
            ))
        
        return history
        
    except Exception as e:
        print(f"❌ History Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch chat history"
        )


@router.delete("/history")
async def clear_chat_history(
    current_user: dict = Depends(get_current_user)
):
    """
    Clear user's chat history
    """
    try:
        user_id = current_user["user_id"]
        db = await get_database()
        
        result = await db.chat_history.delete_many({"user_id": user_id})
        
        return {
            "success": True,
            "message": f"Deleted {result.deleted_count} chat messages"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to clear chat history"
        )


@router.post("/quick-question")
async def quick_question(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Quick question without saving to history (for testing)
    """
    try:
        # Get AI response
        ai_response = await ai_assistant.get_response(
            question=request.message,
            language=request.language,
            context=request.context
        )
        
        response_text = ai_response.get("text", "")
        
        # Generate audio if requested
        audio_url = None
        if request.include_audio and response_text:
            audio_url = await tts_service.text_to_speech(
                text=response_text,
                language=request.language
            )
        
        return {
            "message": response_text,
            "audio_url": audio_url,
            "data": ai_response.get("data"),
            "type": ai_response.get("type", "general")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )
