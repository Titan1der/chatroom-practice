from websockets import WebSocketServerProtocol
from models.chatroom import Chatroom
from datetime import datetime

import json
import websockets

async def chat_service(websocket : WebSocketServerProtocol, room : Chatroom, connected):
    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "chat"
        
        timeFormat = datetime.now().strftime("%H:%M")
        msg = f"{timeFormat} : {event['text']}"
        
        room.chatLog.append(msg)
        
        event = {
            "type" : "chat",
            "chatlog" : room.get_chatlog()
        }
        
        websockets.broadcast(connected, json.dumps(event))