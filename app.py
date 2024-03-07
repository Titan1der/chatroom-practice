import websockets
import json
import asyncio
import secrets
import os
import signal

from websockets import WebSocketServerProtocol
from chatroom import Chatroom
from datetime import datetime


JOIN = {}
WATCH = {}


async def startChatService(websocket : WebSocketServerProtocol, room : Chatroom, connected):
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
        
        #await websockets.broadcast(json.dumps(event))
        websockets.broadcast(connected, json.dumps(event))
        

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
        
        print("Now hosting")
        await websocket.send(json.dumps(event))
        await startChatService(websocket, room, connected)
    
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
        print(f"Joined room - {join_key}")
        
    except KeyError:
        print(f"Room not found")
        return
    
        
    try:
        event = {
            "type" : "chat",
            "chatlog" : room.get_chatlog()
            }
        
        await websocket.send(json.dumps(event))
        await startChatService(websocket, room, connected)
        
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
            print("Server initialization error.")
            

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    
    port = int(os.environ.get("PORT", "8001"))
    
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
