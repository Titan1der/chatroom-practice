from websockets import WebSocketServerProtocol
from models.chatroom import Chatroom
from models.environment_variables import ServerEnv

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


async def host_room(env : ServerEnv, websocket : WebSocketServerProtocol):
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
        
        logging.info(f"Now hosting: join: {join_key} -- watch: {watch_key}")
        await websocket.send(json.dumps(event))
        await update_rooms(env, websocket)
        await chat_service(websocket, room, connected)
    
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]

async def join_room(env : ServerEnv, websocket : WebSocketServerProtocol, join_key):
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



async def update_rooms(env : ServerEnv, websocket : WebSocketServerProtocol):
    rooms = env.get_rooms_list()
    try:
        event = {
            "type" : "rooms",
            "roomList" : rooms,
        }
        await websocket.send(json.dumps(event))
    finally:
        logging.info("Server: sent rooms list to client")


async def handler(websocket : WebSocketServerProtocol):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    
    logging.info(f"Received client event: {event}")
    
    # Get server environemnt global variables
    env = ServerEnv()
    match event["action"]:
        case "host": 
            await host_room(env, websocket)
            
        case "join": 
            await join_room(env, websocket, event["key"])
            
        case "none":
            pass
            # await update_rooms(env, websocket)
                
        case _:
            try:
                event = {
                    "type" : "error",
                    "message" : "unknown_request"
                    }
                await websocket.send(json.dumps(event))
            finally:
                logging.info("Server initialization error.")