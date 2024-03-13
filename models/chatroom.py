import json
import websockets
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class Chatroom(object):
    def __init__(self, room_name, room_key):
        self._room_name = room_name
        self._room_key = room_key
        self._chatLog = []
        self._connected_clients = {}
    
    @property    
    def chatlog(self):
        return self._chatLog
    
    @property
    def connected_clients(self):
        return len(self._connected_clients)
    
    @property
    def name(self):
        return self._room_name
    
    
    async def handle_host_chatroom_request(self, websocket):
        self._connected_clients = {websocket}
        logging.info(f"Number of clients in {self.name}: {self.connected_clients}")
        # Start the chat service for the room
        event = {
            "type" : "host",
            "join" : self._room_key
        }
        
        # Show connected client the room key
        websockets.broadcast(self._connected_clients, json.dumps(event))
        await self.start_chat_service(websocket)
        
    
    async def handle_join_chatroom_request(self, websocket):
        self._connected_clients.add(websocket)
        logging.info(f"Number of clients in {self.name}: {self.connected_clients}")
        # Start the chat service for the room
        await self.start_chat_service(websocket)
        
        
    async def start_chat_service(self, websocket):
        try:
            # Listen for chatroom requests
            async for message in websocket:
                event = json.loads(message)
                assert event["type"] == "chat"
                
                match event["request"]:
                    case "sendMessage":
                        self._chatLog.append(event["text"])
                        
                        event = {
                            "type" : "chat",
                            "chatlog" : self.chatlog
                        }
                        
                        websockets.broadcast(self._connected_clients, json.dumps(event))
                   
                    case _: 
                        self.send_error(websocket, "unknown_error")
                        
        finally:
            self.remove_client(websocket)  

        
    def add_client(self, websocket):
        self._connected_clients.add(websocket)
        logging.info(f"++Added {websocket.id} to room: {self.name}")   


    def remove_client(self, websocket):
        self._connected_clients.remove(websocket)  
        logging.info(f"--Removed {websocket.id} from room: {self.name}")       
                  
    
    # Send error messages to client
    async def send_error(self, websocket, message):
        try:
            event = {
                "type" : "error",
                "message" : message
            }

            await websocket.send(json.dumps(event))
        finally:
            logging.info("**Lobby error")