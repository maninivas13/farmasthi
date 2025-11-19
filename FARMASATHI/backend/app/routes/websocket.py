# routes/websocket.py - WebSocket for Real-time Notifications

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict
from app.utils.security import decode_access_token
import json

router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and store websocket connection"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        print(f"✅ WebSocket connected: {user_id}")
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove websocket connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        print(f"❌ WebSocket disconnected: {user_id}")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def broadcast_to_officers(self, message: dict):
        """Broadcast message to all connected officers"""
        # In a real app, you'd track officer connections separately
        for user_id, connections in self.active_connections.items():
            if user_id.startswith("officer_"):
                for connection in connections:
                    try:
                        await connection.send_json(message)
                    except:
                        pass
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except:
                    pass

# Global connection manager instance
manager = ConnectionManager()

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket, token: str):
    """
    WebSocket endpoint for real-time notifications
    Usage: ws://localhost:8000/ws/notifications?token=<JWT_TOKEN>
    """
    
    # Validate token
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Connect websocket
    await manager.connect(websocket, user_id)
    
    # Send welcome message
    await websocket.send_json({
        "type": "connection",
        "message": "Connected to FarmaSathi notifications",
        "user_id": user_id,
        "role": role
    })
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            
            # Parse message
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                
                elif message.get("type") == "subscribe":
                    # Subscribe to specific channels
                    await websocket.send_json({
                        "type": "subscribed",
                        "channel": message.get("channel")
                    })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)

# Helper function to send notifications through WebSocket
async def send_notification(user_id: str, notification: dict):
    """Send notification to user via WebSocket"""
    await manager.send_personal_message({
        "type": "notification",
        "data": notification
    }, user_id)

async def notify_new_query(query_data: dict):
    """Notify all officers about new query"""
    await manager.broadcast_to_officers({
        "type": "new_query",
        "data": query_data
    })

async def notify_query_reply(farmer_id: str, query_data: dict):
    """Notify farmer about officer reply"""
    await manager.send_personal_message({
        "type": "query_reply",
        "data": query_data
    }, farmer_id)
