import websockets
import json
import asyncio
import secrets
from websockets import WebSocketServerProtocol

from chatroom import Chatroom


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
        
        print("Now hosting")
        await websocket.send(json.dumps(event))
    
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]


async def handler(websocket : WebSocketServerProtocol):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    
    match event["action"]:
        case "host": 
            await hostRoom(websocket)
        
        case _:
            print("Server initialization error.")
            
        
    


async def main():
    async with websockets.serve(handler, "localhost", 8001):
        print("Now listening on port8001:")
        await asyncio.Future() # run infinitely

if __name__ == "__main__":
    asyncio.run(main())
