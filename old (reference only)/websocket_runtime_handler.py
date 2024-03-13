from websockets import WebSocketServerProtocol
from models.chatroom import Chatroom
from datetime import datetime
from models.environment_variables import ServerEnv

import json
import websockets


async def chat_service(room : Chatroom, connected):
    timeFormat = datetime.now().strftime("%H:%M")
    msg = f"{timeFormat} : {event['text']}"
    
    room.chatLog.append(msg)
    
    event = {
        "type" : "chat",
        "chatlog" : room.get_chatlog()
    }

    websockets.broadcast(connected, json.dumps(event))


async def host_service():
    pass



async def websocket_runtime_handler(env : ServerEnv, websocket : WebSocketServerProtocol, room=None, connected=None):
    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "runtime"
        
        match event["service"]:
            case "chat": chat_service(room, connected)
            case "host": host_service()
                