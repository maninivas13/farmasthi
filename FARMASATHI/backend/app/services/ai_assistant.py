# ai_assistant.py - AI Chatbot Service with Multi-Provider Support

import os
import json
import httpx
from typing import Dict, List, Optional
from datetime import datetime

class AIAssistant:
    """
    AI Assistant for FarmaSathi Platform
    Supports OpenAI, Google Gemini, and fallback to rule-based responses
    """
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "")
        self.provider = self._detect_provider()
        
    def _detect_provider(self) -> str:
        """Detect which AI provider is available"""
        if self.openai_key:
            return "openai"
        elif self.gemini_key:
            return "gemini"
        else:
            return "fallback"
    
    async def get_response(
        self, 
        question: str, 
        language: str = "en",
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Get AI response for farmer's question
        
        Args:
            question: User's question
            language: Response language (en, hi, te, ta, bn, mr)
            context: Additional context (location, crop type, etc.)
        
        Returns:
            Dict with 'text' and 'audio_url' keys
        """
        try:
            # Check if question is about weather
            if self._is_weather_query(question):
                return await self._handle_weather_query(question, language, context)
            
            # Check if question is about market prices
            elif self._is_market_query(question):
                return await self._handle_market_query(question, language, context)
            
            # General agricultural question
            else:
                return await self._handle_general_query(question, language, context)
                
        except Exception as e:
            print(f"❌ AI Assistant Error: {str(e)}")
            return await self._fallback_response(question, language)
    
    def _is_weather_query(self, question: str) -> bool:
        """Check if question is about weather"""
        weather_keywords = [
            'weather', 'temperature', 'rain', 'forecast', 'climate',
            'मौसम', 'बारिश', 'तापमान',  # Hindi
            'వాతావరణం', 'వర్షం',  # Telugu
            'வானிலை', 'மழை',  # Tamil
            'আবহাওয়া', 'বৃষ্টি',  # Bengali
            'हवामान', 'पाऊस'  # Marathi
        ]
        return any(keyword in question.lower() for keyword in weather_keywords)
    
    def _is_market_query(self, question: str) -> bool:
        """Check if question is about market prices"""
        market_keywords = [
            'price', 'market', 'sell', 'rate', 'cost', 'mandi',
            'कीमत', 'बाजार', 'भाव', 'मंडी',  # Hindi
            'ధర', 'మార్కెట్',  # Telugu
            'விலை', 'சந்தை',  # Tamil
            'মূল্য', 'বাজার',  # Bengali
            'किंमत', 'बाजार'  # Marathi
        ]
        return any(keyword in question.lower() for keyword in market_keywords)
    
    async def _handle_weather_query(
        self, 
        question: str, 
        language: str,
        context: Optional[Dict]
    ) -> Dict:
        """Handle weather-related queries"""
        location = context.get("location", "your area") if context else "your area"
        
        # Get real weather data if API key available
        if self.weather_api_key and self.weather_api_key != "your_weather_api_key_here":
            weather_data = await self._fetch_real_weather(location)
        else:
            # Use simulated data
            weather_data = {
                "temp": 28,
                "humidity": 65,
                "condition": "Partly Cloudy",
                "rainfall": "20% chance",
                "wind": "12 km/h"
            }
        
        # Generate response using AI or template
        if self.provider == "openai":
            response_text = await self._get_openai_response(
                question, language, weather_data
            )
        elif self.provider == "gemini":
            response_text = await self._get_gemini_response(
                question, language, weather_data
            )
        else:
            response_text = self._generate_weather_response(weather_data, language)
        
        return {
            "text": response_text,
            "data": weather_data,
            "type": "weather"
        }
    
    async def _handle_market_query(
        self, 
        question: str, 
        language: str,
        context: Optional[Dict]
    ) -> Dict:
        """Handle market price queries"""
        # Extract crop name from question
        crop = self._extract_crop_name(question)
        
        # Get market data
        market_data = await self._fetch_market_prices(crop)
        
        # Generate response
        if self.provider == "openai":
            response_text = await self._get_openai_response(
                question, language, market_data
            )
        elif self.provider == "gemini":
            response_text = await self._get_gemini_response(
                question, language, market_data
            )
        else:
            response_text = self._generate_market_response(market_data, crop, language)
        
        return {
            "text": response_text,
            "data": market_data,
            "type": "market"
        }
    
    async def _handle_general_query(
        self, 
        question: str, 
        language: str,
        context: Optional[Dict]
    ) -> Dict:
        """Handle general agricultural queries"""
        if self.provider == "openai":
            response_text = await self._get_openai_response(question, language)
        elif self.provider == "gemini":
            response_text = await self._get_gemini_response(question, language)
        else:
            response_text = await self._get_rule_based_response(question, language)
        
        return {
            "text": response_text,
            "type": "general"
        }
    
    async def _get_openai_response(
        self, 
        question: str, 
        language: str,
        data: Optional[Dict] = None
    ) -> str:
        """Get response from OpenAI GPT"""
        try:
            system_prompt = self._get_system_prompt(language)
            user_prompt = question
            
            if data:
                user_prompt = f"{question}\n\nContext Data: {json.dumps(data)}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"OpenAI API error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ OpenAI Error: {str(e)}")
            fallback = await self._fallback_response(question, language)
            return fallback["text"]
    
    async def _get_gemini_response(
        self, 
        question: str, 
        language: str,
        data: Optional[Dict] = None
    ) -> str:
        """Get response from Google Gemini"""
        try:
            system_instruction = self._get_system_prompt(language)
            user_prompt = question
            
            if data:
                user_prompt = f"{question}\n\nContext: {json.dumps(data)}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.gemini_key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{
                            "parts": [{
                                "text": f"{system_instruction}\n\n{user_prompt}"
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 500
                        }
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    raise Exception(f"Gemini API error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Gemini Error: {str(e)}")
            fallback = await self._fallback_response(question, language)
            return fallback["text"]
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt for AI model"""
        prompts = {
            "en": """You are an expert agricultural assistant helping Indian farmers. 
Provide practical, actionable advice in simple language. Include specific steps when possible.
Keep responses concise (under 200 words). Be empathetic and encouraging.""",
            
            "hi": """आप एक कृषि विशेषज्ञ सहायक हैं जो भारतीय किसानों की मदद कर रहे हैं।
सरल भाषा में व्यावहारिक सलाह दें। संभव हो तो विशिष्ट कदम शामिल करें।
संक्षिप्त उत्तर दें (200 शब्दों से कम)। सहानुभूतिपूर्ण और प्रोत्साहक बनें।"""
        }
        
        return prompts.get(language, prompts["en"])
    
    async def _get_rule_based_response(self, question: str, language: str) -> str:
        """Rule-based fallback response"""
        question_lower = question.lower()
        
        # Pest control
        if any(word in question_lower for word in ['pest', 'insect', 'bug', 'कीट']):
            return self._get_translation(language, "pest_response")
        
        # Disease
        elif any(word in question_lower for word in ['disease', 'fungus', 'rot', 'रोग']):
            return self._get_translation(language, "disease_response")
        
        # Fertilizer
        elif any(word in question_lower for word in ['fertilizer', 'nutrient', 'खाद']):
            return self._get_translation(language, "fertilizer_response")
        
        # Irrigation
        elif any(word in question_lower for word in ['water', 'irrigation', 'सिंचाई', 'पानी']):
            return self._get_translation(language, "irrigation_response")
        
        # Default
        else:
            return self._get_translation(language, "general_response")
    
    def _get_translation(self, language: str, key: str) -> str:
        """Get translated response"""
        responses = {
            "pest_response": {
                "en": "For pest control, try neem oil spray (10ml per liter of water). Spray early morning or evening. Repeat after 7 days if needed. For severe infestation, consult an agricultural officer.",
                "hi": "कीट नियंत्रण के लिए, नीम के तेल का स्प्रे (10 मिली प्रति लीटर पानी) आजमाएं। सुबह या शाम को छिड़काव करें। आवश्यकता हो तो 7 दिन बाद दोहराएं। गंभीर संक्रमण के लिए कृषि अधिकारी से परामर्श लें।"
            },
            "disease_response": {
                "en": "For plant diseases, remove infected parts immediately. Improve air circulation. Avoid overhead watering. Apply copper-based fungicide if needed. Maintain proper field sanitation.",
                "hi": "पौधों की बीमारियों के लिए, संक्रमित भागों को तुरंत हटा दें। हवा का संचार सुधारें। पत्तियों पर पानी डालने से बचें। आवश्यकता हो तो कॉपर-आधारित फफूंदनाशक लगाएं। खेत की स्वच्छता बनाए रखें।"
            },
            "fertilizer_response": {
                "en": "Get soil tested first to determine nutrient needs. Apply balanced NPK fertilizer as per soil test results. Use organic manure to improve soil health. Apply in split doses for better results.",
                "hi": "पोषक तत्वों की जरूरत निर्धारित करने के लिए पहले मिट्टी की जांच करवाएं। मिट्टी परीक्षण के अनुसार संतुलित एनपीके खाद डालें। मिट्टी के स्वास्थ्य में सुधार के लिए जैविक खाद का उपयोग करें। बेहतर परिणामों के लिए विभाजित खुराक में डालें।"
            },
            "irrigation_response": {
                "en": "Water early morning or late evening to reduce evaporation. Use drip irrigation for water efficiency. Check soil moisture before watering. Avoid waterlogging which can damage roots.",
                "hi": "वाष्पीकरण कम करने के लिए सुबह जल्दी या शाम को देर से पानी दें। पानी की दक्षता के लिए ड्रिप सिंचाई का उपयोग करें। पानी देने से पहले मिट्टी की नमी जांचें। जलभराव से बचें जो जड़ों को नुकसान पहुंचा सकता है।"
            },
            "general_response": {
                "en": "I'm here to help with your agricultural questions. I can provide information about pest control, diseases, fertilizers, irrigation, weather, and market prices. Please ask your specific question.",
                "hi": "मैं आपके कृषि प्रश्नों में मदद के लिए यहां हूं। मैं कीट नियंत्रण, बीमारियों, उर्वरकों, सिंचाई, मौसम और बाजार कीमतों के बारे में जानकारी प्रदान कर सकता हूं। कृपया अपना विशिष्ट प्रश्न पूछें।"
            }
        }
        
        return responses.get(key, {}).get(language, responses[key]["en"])
    
    async def _fetch_real_weather(self, location: str) -> Dict:
        """Fetch real weather data from OpenWeatherMap API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "q": location,
                        "appid": self.weather_api_key,
                        "units": "metric"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "condition": data["weather"][0]["description"],
                        "wind": f"{data['wind']['speed']} m/s",
                        "rainfall": "Check forecast for details"
                    }
        except Exception as e:
            print(f"❌ Weather API Error: {str(e)}")
        
        # Fallback data
        return {
            "temp": 28,
            "humidity": 65,
            "condition": "Partly Cloudy",
            "wind": "12 km/h"
        }
    
    async def _fetch_market_prices(self, crop: str) -> Dict:
        """Fetch market prices for crop"""
        # This would connect to real market API or database
        market_data = {
            "rice": {"min": 1800, "max": 2200, "avg": 2000, "unit": "₹/quintal", "trend": "stable"},
            "wheat": {"min": 1900, "max": 2100, "avg": 2000, "unit": "₹/quintal", "trend": "rising"},
            "cotton": {"min": 5500, "max": 6000, "avg": 5750, "unit": "₹/quintal", "trend": "falling"},
            "tomato": {"min": 800, "max": 1200, "avg": 1000, "unit": "₹/quintal", "trend": "volatile"},
            "potato": {"min": 600, "max": 900, "avg": 750, "unit": "₹/quintal", "trend": "stable"},
        }
        
        return market_data.get(crop.lower(), {
            "min": 0, "max": 0, "avg": 0, "unit": "₹/quintal", "trend": "unknown"
        })
    
    def _extract_crop_name(self, question: str) -> str:
        """Extract crop name from question"""
        crops = ['rice', 'wheat', 'cotton', 'tomato', 'potato', 'maize', 'sugarcane',
                 'धान', 'गेहूं', 'कपास', 'टमाटर']
        
        for crop in crops:
            if crop in question.lower():
                # Map to English name
                crop_map = {'धान': 'rice', 'गेहूं': 'wheat', 'कपास': 'cotton', 'टमाटर': 'tomato'}
                return crop_map.get(crop, crop)
        
        return "general"
    
    def _generate_weather_response(self, weather_data: Dict, language: str) -> str:
        """Generate weather response text"""
        if language == "hi":
            return f"आज का मौसम: तापमान {weather_data['temp']}°C, आर्द्रता {weather_data['humidity']}%, स्थिति {weather_data['condition']}। हवा की गति {weather_data['wind']}।"
        else:
            return f"Today's weather: Temperature {weather_data['temp']}°C, Humidity {weather_data['humidity']}%, Condition {weather_data['condition']}. Wind speed {weather_data['wind']}."
    
    def _generate_market_response(self, market_data: Dict, crop: str, language: str) -> str:
        """Generate market response text"""
        if market_data.get("avg", 0) == 0:
            return "Price data not available for this crop currently." if language == "en" else "इस फसल के लिए कीमत डेटा वर्तमान में उपलब्ध नहीं है।"
        
        if language == "hi":
            return f"{crop} की कीमत: न्यूनतम ₹{market_data['min']}, अधिकतम ₹{market_data['max']}, औसत ₹{market_data['avg']} प्रति क्विंटल। बाजार प्रवृत्ति: {market_data['trend']}।"
        else:
            return f"{crop.title()} prices: Min ₹{market_data['min']}, Max ₹{market_data['max']}, Avg ₹{market_data['avg']} per quintal. Market trend: {market_data['trend']}."
    
    async def _fallback_response(self, question: str, language: str) -> Dict:
        """Fallback response when AI services fail"""
        response_text = await self._get_rule_based_response(question, language)
        return {
            "text": response_text,
            "type": "fallback"
        }


# Singleton instance
ai_assistant = AIAssistant()
