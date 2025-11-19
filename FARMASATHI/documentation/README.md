# 🌾 AgriAssist - AI-Powered Agricultural Platform

> Complete full-stack agricultural assistance platform with AI chatbot, multi-language support, real-time notifications, and comprehensive farmer-officer workflow.

![Version](https://img.shields.io/badge/version-2.0.0-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-teal)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Setup Guide](#-setup-guide)
- [AI Chatbot](#-ai-chatbot)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)

---

## ✨ Features

### **For Farmers**
- 🌐 **Multi-language Support**: 6 Indian languages (English, Hindi, Telugu, Tamil, Bengali, Marathi)
- 🎤 **Voice Recording**: Submit queries via voice
- 📸 **Image Upload**: Upload crop images for pest/disease detection
- 🤖 **AI Chatbot**: 24/7 instant support with text and audio responses
- 🔔 **Real-time Notifications**: Get instant updates on query status
- 📜 **Query History**: Track all previous queries and responses
- ☁️ **Weather Widget**: Local weather information
- 💰 **Market Prices**: Real-time crop price information

### **For Officers**
- 📊 **Analytics Dashboard**: Comprehensive statistics and charts
- 📝 **Query Management**: Assign, respond, and track queries
- 🎯 **Priority System**: Filter by urgency and status
- 📈 **Performance Metrics**: Track resolution rates and response times
- 🔔 **Real-time Alerts**: Instant notifications for new queries
- 📄 **Export Data**: Download reports and statistics

### **AI-Powered Features**
- 🤖 **Intelligent Chatbot**: OpenAI GPT or Google Gemini integration
- 🗣️ **Text-to-Speech**: Audio responses in 6 languages
- 🌤️ **Weather Integration**: Real-time weather from OpenWeatherMap
- 💹 **Market Intelligence**: Live crop price tracking
- 🔍 **Smart Search**: Context-aware query processing

---

## 🚀 Quick Start

### **Prerequisites**
```bash
- Python 3.9+
- MongoDB 4.4+
- Node.js (optional, for frontend alternatives)
```

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/agriassist.git
cd agriassist
```

### **2. Install Backend Dependencies**
```bash
cd frontend/backend
pip install -r requirements.txt
```

### **3. Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### **4. Start MongoDB**
```bash
mongod --dbpath="C:\data\db"
```

### **5. Start Backend**
```bash
python run.py
# Backend runs on http://localhost:8000
```

### **6. Start Frontend**
```bash
cd frontend
python -m http.server 3000
# Frontend runs on http://localhost:3000
```

### **7. Open Application**
```
http://localhost:3000
```

✅ **That's it!** You should see the AgriAssist homepage with the AI chatbot button in the bottom-right corner.

---

## 📁 Project Structure

```
ai.farmer/
├── frontend/
│   ├── backend/              # FastAPI Backend
│   │   ├── app/
│   │   │   ├── models/       # Pydantic models
│   │   │   ├── routes/       # API endpoints
│   │   │   ├── services/     # AI & TTS services
│   │   │   ├── utils/        # Security & helpers
│   │   │   ├── database.py   # MongoDB connection
│   │   │   └── main.py       # FastAPI app
│   │   ├── uploads/          # File storage
│   │   ├── requirements.txt  # Python dependencies
│   │   ├── .env             # Configuration
│   │   └── run.py           # Startup script
│   │
│   ├── index.html           # Farmer interface
│   ├── dashboard.html       # Officer dashboard
│   ├── login.html           # Authentication
│   ├── style.css            # Global styles
│   ├── api-config.js        # API client
│   ├── ai-chatbot.js        # Chatbot UI ⭐ NEW
│   ├── main.js              # Farmer logic
│   ├── dashboard.js         # Officer logic
│   ├── translation.js       # Multi-language
│   ├── voice-recorder.js    # Voice input
│   └── notifications.js     # Real-time updates
│
├── AI_CHATBOT_GUIDE.txt     # Chatbot setup ⭐ NEW
├── AI_CHATBOT_SUMMARY.md    # Feature overview ⭐ NEW
├── CHATBOT_VISUAL_GUIDE.txt # UI documentation ⭐ NEW
├── SETUP_GUIDE.txt          # Complete setup
└── README.md                # This file
```

---

## 🛠️ Technology Stack

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5.3
- Chart.js (Analytics)
- Web Audio API (Voice recording)
- WebSocket (Real-time updates)

### **Backend**
- **FastAPI** 0.104+ (Python web framework)
- **Motor** 3.3+ (Async MongoDB driver)
- **Pydantic** 2.5+ (Data validation)
- **JWT** (Authentication)
- **WebSocket** (Real-time communication)

### **AI Services** ⭐
- **OpenAI GPT-3.5** (Intelligent responses)
- **Google Gemini** (Free alternative)
- **gTTS** (Text-to-Speech)
- **OpenWeatherMap** (Weather data)

### **Database**
- **MongoDB** 4.4+ (Document store)
- Collections: users, queries, responses, notifications, chat_history

---

## 📖 Setup Guide

### **Detailed Setup**
For complete installation instructions, see:
- **[SETUP_GUIDE.txt](./SETUP_GUIDE.txt)** - General platform setup
- **[AI_CHATBOT_GUIDE.txt](./AI_CHATBOT_GUIDE.txt)** - AI chatbot setup ⭐

### **Quick Configuration**

#### **1. MongoDB Setup**
```bash
# Local MongoDB
mongod --dbpath="C:\data\db"

# OR MongoDB Atlas (Cloud)
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/agriassist
```

#### **2. API Keys (.env file)**
```env
# AI Chatbot (Choose one)
OPENAI_API_KEY=sk-your-openai-key        # $0.002/request
GEMINI_API_KEY=your-gemini-key           # FREE

# Weather (Optional)
WEATHER_API_KEY=your-openweather-key     # FREE

# Security
SECRET_KEY=your-secret-key-change-this
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey
- Weather: https://openweathermap.org/api

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**New AI Dependencies:**
- `openai==1.6.1` - OpenAI GPT integration
- `google-generativeai==0.3.2` - Gemini AI
- `gTTS==2.5.0` - Text-to-Speech
- `pydub==0.25.1` - Audio processing

---

## 🤖 AI Chatbot

### **What's New** ⭐

The platform now includes a powerful AI chatbot assistant that provides:

1. **Instant Answers**: Weather, market prices, farming advice
2. **Audio Responses**: Text-to-speech in 6 languages
3. **Smart Context**: Remembers location and conversation
4. **Quick Actions**: One-click common queries
5. **24/7 Availability**: No waiting for officers

### **Chatbot Features**

```
🌤️ Weather Queries
   "What is today's weather?"
   → Temperature, humidity, forecast + audio

💰 Market Prices
   "What is the rice price?"
   → Min/max/avg prices, trends + audio

🐛 Pest Control
   "How to control pests in tomatoes?"
   → Treatment steps, recommendations + audio

🌿 Disease Help
   "My wheat has yellow leaves"
   → Diagnosis, solutions, prevention + audio

📚 General Advice
   "When to plant cotton?"
   → Season, preparation, tips + audio
```

### **How to Use**

1. **Click** green chat button (bottom-right)
2. **Type** your question or use quick actions
3. **Get** instant text + audio response
4. **Listen** to answer in your language

### **Documentation**
- **[AI_CHATBOT_SUMMARY.md](./AI_CHATBOT_SUMMARY.md)** - Feature overview
- **[AI_CHATBOT_GUIDE.txt](./AI_CHATBOT_GUIDE.txt)** - Setup & config
- **[CHATBOT_VISUAL_GUIDE.txt](./CHATBOT_VISUAL_GUIDE.txt)** - UI guide

---

## 📚 API Documentation

### **Base URL**
```
http://localhost:8000
```

### **Interactive Docs**
```
http://localhost:8000/docs    # Swagger UI
http://localhost:8000/redoc   # ReDoc
```

### **Authentication**
All protected endpoints require JWT token:
```bash
Authorization: Bearer <token>
```

### **Main Endpoints**

#### **Authentication**
```http
POST /api/auth/register    # Register new user
POST /api/auth/login       # Login and get token
GET  /api/auth/me          # Get current user
```

#### **Queries**
```http
POST /api/queries/submit       # Submit new query
GET  /api/queries/history      # Get user queries
GET  /api/queries/{id}         # Get query details
PUT  /api/queries/{id}/assign  # Assign to officer
PUT  /api/queries/{id}/reply   # Add officer response
GET  /api/queries/statistics   # Get statistics
```

#### **File Uploads**
```http
POST /api/upload/image    # Upload crop image
POST /api/upload/voice    # Upload voice recording
```

#### **AI Chatbot** ⭐
```http
POST /api/chat/message         # Send chat message
GET  /api/chat/history         # Get chat history
DELETE /api/chat/history       # Clear history
POST /api/chat/quick-question  # Quick Q&A (no history)
```

#### **Data Services**
```http
POST /api/weather          # Get weather data
POST /api/market-prices    # Get crop prices
POST /api/ai-analysis      # AI query analysis
```

#### **WebSocket**
```websocket
WS /ws/notifications?token=<jwt>    # Real-time updates
```

---

## 📸 Screenshots

### **Farmer Interface**
```
┌─────────────────────────────────────────┐
│  🌱 AgriAssist              [Login]     │
├─────────────────────────────────────────┤
│  AI-Based Farmer Query Support          │
│  [Ask a Query] [Dashboard]              │
├─────────────────────────────────────────┤
│  Our Services:                          │
│  🐛 Pest Help  ☁️ Weather  📈 Market   │
├─────────────────────────────────────────┤
│  Ask a Query:                           │
│  [Name] [Location] [Crop]               │
│  [Description...]                       │
│  [Upload Image] [Record Voice]          │
│  [Submit Query]                         │
└─────────────────────────────────────────┘
                           [💬 AI Chat] ← NEW
```

### **AI Chatbot** ⭐
```
┌──────────────────────┐
│ 🤖 AgriAssist AI  🗑️ │
├──────────────────────┤
│ ☀️ Weather  💰 Price │
│ 🐛 Pest  🌿 Disease  │
├──────────────────────┤
│ 🤖 Hello! Ask me     │
│    anything...       │
│                      │
│ 👤 What's weather?   │
│                      │
│ 🤖 Temperature: 28°C │
│    🔊 Play Audio     │
│    ┌──────────────┐  │
│    │ 🌡️ 28°C      │  │
│    │ 💧 65%       │  │
│    └──────────────┘  │
├──────────────────────┤
│ Type question...  📤 │
└──────────────────────┘
```

### **Officer Dashboard**
```
┌─────────────────────────────────────────┐
│ 🌱 AgriAssist                           │
│ Officer Dashboard                       │
├─────────────────────────────────────────┤
│ Stats:                                  │
│ ┌──────┬──────┬──────┬──────┐          │
│ │Total │Open  │Assgn │Resol │          │
│ │ 247  │ 12   │ 35   │ 200  │          │
│ └──────┴──────┴──────┴──────┘          │
├─────────────────────────────────────────┤
│ Recent Queries:                         │
│ [ID] [Farmer] [Crop] [Status] [Action] │
│ ...                                     │
└─────────────────────────────────────────┘
                           [💬 AI Chat] ← NEW
```

---

## 🧪 Testing

### **Test Backend**
```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

### **Test Chatbot**
1. Open http://localhost:3000
2. Login or register
3. Click green chat button (bottom-right)
4. Ask: "What is today's weather?"
5. Should get text + audio response

### **Test Full Flow**
1. **Register** as farmer
2. **Submit** query with image/voice
3. **Chat** with AI assistant
4. **Check** notifications
5. **View** query history

---

## 🔧 Configuration

### **Environment Variables**
```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=agriassist_db

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI Services ⭐
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
WEATHER_API_KEY=...

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### **Customize Chatbot**

**Change AI Provider:**
Edit `.env` - set `OPENAI_API_KEY` or `GEMINI_API_KEY`

**Modify Response Style:**
Edit `backend/app/services/ai_assistant.py` line 195

**Change UI Colors:**
Edit `frontend/style.css` CSS variables

**Add Quick Actions:**
Edit `frontend/ai-chatbot.js` lines 29-44

---

## 📊 Database Schema

### **Collections**

#### **users**
```javascript
{
  _id: ObjectId,
  name: string,
  phone: string,
  hashed_password: string,
  role: "farmer" | "officer",
  created_at: datetime
}
```

#### **queries**
```javascript
{
  _id: ObjectId,
  farmer_id: string,
  farmer_name: string,
  location: string,
  crop_type: string,
  query_text: string,
  image_url: string,
  voice_url: string,
  status: "open" | "assigned" | "resolved",
  urgency: "normal" | "high",
  created_at: datetime
}
```

#### **chat_history** ⭐ NEW
```javascript
{
  _id: ObjectId,
  user_id: string,
  user_message: string,
  bot_response: string,
  audio_url: string,
  language: string,
  response_type: "weather" | "market" | "general",
  timestamp: datetime
}
```

---

## 🚀 Deployment

### **Production Checklist**
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=false`
- [ ] Use MongoDB Atlas (cloud)
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Set up CDN for static files
- [ ] Configure backup strategy
- [ ] Monitor error logs
- [ ] Set up alerts

### **Deploy Options**
- **Heroku**: `heroku create && git push heroku main`
- **AWS**: EC2 + RDS + S3
- **Azure**: App Service + CosmosDB
- **Google Cloud**: Cloud Run + Firestore
- **DigitalOcean**: Droplet + Managed MongoDB

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Development Setup**
```bash
git clone https://github.com/yourusername/agriassist.git
cd agriassist
pip install -r requirements.txt
# Make your changes
pytest  # Run tests
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Bootstrap 5 for UI components
- FastAPI for backend framework
- OpenAI for GPT integration
- Google for Gemini and gTTS
- MongoDB for database
- All contributors and supporters

---

## 📞 Support

- **Documentation**: See guides in repository
- **Issues**: [GitHub Issues](https://github.com/yourusername/agriassist/issues)
- **Email**: support@agriassist.com
- **Discord**: [Join our community](https://discord.gg/agriassist)

---

## 🗺️ Roadmap

### **v2.1 (Next Release)**
- [ ] Mobile app (React Native)
- [ ] SMS notifications
- [ ] WhatsApp integration
- [ ] Offline mode

### **v3.0 (Future)**
- [ ] Crop disease detection (CNN)
- [ ] Yield prediction (ML models)
- [ ] Soil testing integration
- [ ] Farm management tools

---

## ⭐ Star Us!

If this project helped you, please give it a ⭐️ on GitHub!

---

<div align="center">

**Made with ❤️ for Indian Farmers**

🌾 AgriAssist - Empowering Agriculture with AI 🤖

[Website](https://agriassist.com) · [Documentation](./docs) · [Report Bug](https://github.com/yourusername/agriassist/issues) · [Request Feature](https://github.com/yourusername/agriassist/issues)

</div>
