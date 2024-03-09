from websockets import WebSocketServerProtocol
from models.chatroom import Chatroom

from controller.functions_py.chat_service_handler import chat_service

import secrets
import json

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

JOIN = {}
WATCH = {}


async def hostRoom(websocket : WebSocketServerProtocol):
    room = Chatroom()
    connected = {websocket}
    
    join_key = secrets.token_urlsafe(12)
    watch_key = secrets.token_urlsafe(12)
    
    JOIN[join_key] = room, connected
    WATCH[watch_key] = room, connected
       
    try:  
        event = {
            "type" : "host",
            "join" : join_key,
            "watch" : watch_key
            }
        
        logging.info(f"Now hosting: join:{join_key} - watch{watch_key}")
        await websocket.send(json.dumps(event))
        await chat_service(websocket, room, connected)
    
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]

async def joinRoom(websocket : WebSocketServerProtocol, join_key):
    #if join_key not in JOIN:
    if join_key not in JOIN:
        raise AssertionError()
    
    room, connected = JOIN[join_key]
    connected.add(websocket)
    try:
        event = {
            "type" : "join",
            "userName" : "Chatter 2"
            }
        
        await websocket.send(json.dumps(event))
        logging.info(f"Joined room - {join_key}")
        
    except KeyError:
        logging.info(f"Room not found")
        return
    
        
    try:
        event = {
            "type" : "chat",
            "chatlog" : room.get_chatlog()
            }
        
        await websocket.send(json.dumps(event))
        await chat_service(websocket, room, connected)
        
    finally:
        connected.remove(websocket) 


async def handler(websocket : WebSocketServerProtocol):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    
    match event["action"]:
        case "host": 
            await hostRoom(websocket)
            
        case "join": 
            await joinRoom(websocket, event["key"])
            
        case _:
            logging.info("Server initialization error.")