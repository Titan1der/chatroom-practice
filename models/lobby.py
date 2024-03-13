import secrets
import json
from models.chatroom import Chatroom

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class Lobby(object):
    def __init__(self, lobby_name):
        self._lobby_name = lobby_name
        self._chatrooms = {}
        self._connected_clients = set()
        
    # Handler for lobby requests
    async def handle_lobby_requests(self, websocket):
        # Ideally to send the user to a lobby close to his region
        self.add_client(websocket)
        logging.info(f"Number of client in {self.name}: {self.num_of_connected_clients}")
        
        try:
            # Listen for messages on the client socket
            async for message in websocket:
                event = json.loads(message)
                assert event["type"] == "runtime"
                
                # Ack request
                logging.info(f"Received request from {websocket.id}: {event}")
                
                match event["request"]:
                    case "host": 
                        room_key = secrets.token_urlsafe(12)
                        room = Chatroom(event["room_name"], room_key)
                        self.add_chatroom(room)
                        
                        logging.info(f"{self.name} added a new room: {room.name}")
                        await room.handle_host_chatroom_request(websocket)
                        
                    case "join": 
                        room_key = event["join_key"]
                        assert room_key in self._chatrooms
                        room = self._chatrooms[room_key]
                        
                        await room.handle_join_chatroom_request(websocket)
                    
                    case _: 
                        self.send_error(websocket, "unknown_error")
                        
                
        finally:
            self.remove_client(websocket)
            
        
        
    def add_client(self, websocket):
        self._connected_clients.add(websocket)
        logging.info(f"++Added {websocket.id} to lobby: {self._lobby_name}")
        
        
    def remove_client(self, websocket):
        self._connected_clients.remove(websocket)
        logging.info(f"--Removed {websocket.id} from lobby: {self._lobby_name}")
        
        
    def add_chatroom(self, chatroomObj : Chatroom):
        self._chatrooms[chatroomObj._room_key] = chatroomObj
        
        
    @property
    def num_of_connected_clients(self):
        return len(self._connected_clients)
    
    @property
    def name(self):
        return self._lobby_name
    
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