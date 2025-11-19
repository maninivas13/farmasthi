# routes/uploads.py - File Upload Routes

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from app.utils.security import get_current_user
from typing import Optional
import os
import aiofiles
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/upload", tags=["File Uploads"])

# Upload directories
UPLOAD_DIR = "uploads"
IMAGE_DIR = os.path.join(UPLOAD_DIR, "images")
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")

# Create upload directories if they don't exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".webm"}

# Max file sizes (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 20 * 1024 * 1024  # 20MB

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()

def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with timestamp and UUID"""
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload image file for query"""
    
    # Validate file extension
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_IMAGE_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(IMAGE_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Return file path
    return {
        "success": True,
        "filename": unique_filename,
        "path": f"/uploads/images/{unique_filename}",
        "size": len(content),
        "content_type": file.content_type
    }

@router.post("/voice")
async def upload_voice(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload voice/audio file for query"""
    
    # Validate file extension
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_AUDIO_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(AUDIO_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Return file path
    return {
        "success": True,
        "filename": unique_filename,
        "path": f"/uploads/audio/{unique_filename}",
        "size": len(content),
        "content_type": file.content_type,
        "duration": None  # Could be extracted with librosa or similar
    }

@router.delete("/image/{filename}")
async def delete_image(
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete uploaded image"""
    file_path = os.path.join(IMAGE_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    try:
        os.remove(file_path)
        return {"success": True, "message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )

@router.delete("/voice/{filename}")
async def delete_voice(
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete uploaded voice file"""
    file_path = os.path.join(AUDIO_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    try:
        os.remove(file_path)
        return {"success": True, "message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )
