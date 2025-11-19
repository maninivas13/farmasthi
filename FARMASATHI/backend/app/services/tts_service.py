# tts_service.py - Text-to-Speech Service for Multi-language Audio Responses

import os
import hashlib
from typing import Optional
from gtts import gTTS
import uuid
from pathlib import Path

class TTSService:
    """
    Text-to-Speech service for converting AI responses to audio
    Supports multiple Indian languages
    """
    
    def __init__(self):
        self.audio_dir = "uploads/audio/tts"
        self._ensure_audio_directory()
        
        # Language code mapping
        self.lang_map = {
            "en": "en",
            "hi": "hi",
            "te": "te",
            "ta": "ta",
            "bn": "bn",
            "mr": "mr"
        }
    
    def _ensure_audio_directory(self):
        """Ensure audio directory exists"""
        Path(self.audio_dir).mkdir(parents=True, exist_ok=True)
    
    async def text_to_speech(
        self, 
        text: str, 
        language: str = "en",
        slow: bool = False
    ) -> str:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            language: Language code (en, hi, te, ta, bn, mr)
            slow: Speak slowly for better clarity
        
        Returns:
            Relative path to audio file
        """
        try:
            # Get language code
            lang_code = self.lang_map.get(language, "en")
            
            # Generate unique filename based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
            filename = f"{text_hash}_{language}_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(self.audio_dir, filename)
            
            # Check if file already exists (cache)
            if os.path.exists(filepath):
                return f"/uploads/audio/tts/{filename}"
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            tts.save(filepath)
            
            print(f"✅ Generated TTS audio: {filename}")
            return f"/uploads/audio/tts/{filename}"
            
        except Exception as e:
            print(f"❌ TTS Error: {str(e)}")
            return ""
    
    async def generate_with_fallback(
        self,
        text: str,
        language: str = "en"
    ) -> Optional[str]:
        """
        Generate audio with fallback to English if target language fails
        """
        try:
            # Try target language first
            audio_path = await self.text_to_speech(text, language)
            if audio_path:
                return audio_path
            
            # Fallback to English if supported language fails
            if language != "en":
                print(f"⚠️ Falling back to English for TTS")
                return await self.text_to_speech(text, "en")
            
            return None
            
        except Exception as e:
            print(f"❌ TTS Fallback Error: {str(e)}")
            return None
    
    def cleanup_old_files(self, max_age_days: int = 7):
        """Clean up old TTS files to save disk space"""
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            
            for filename in os.listdir(self.audio_dir):
                filepath = os.path.join(self.audio_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"🗑️ Cleaned up old TTS file: {filename}")
                    
        except Exception as e:
            print(f"❌ Cleanup Error: {str(e)}")


# Singleton instance
tts_service = TTSService()
