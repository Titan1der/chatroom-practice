import os
import websockets
import json

from controller.functions_py.constants import *
from websockets import WebSocketServerProtocol

from models.lobby import Lobby

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class AppServer(object):
    def __init__(self):
        self._lobbies = {}
        self._connected_clients = set()
        logging.info("App server started")
        
        # Create the default lobby that the server hosts
        self.create_lobby()
        
        
    # Create a default lobby
    def create_lobby(self):
        self.add_lobby("default_lobby", Lobby("DefaultLobby"))
        
        
    # Main handler for client requests
    async def handle_requests(self, websocket : WebSocketServerProtocol):
        try:
            message = await websocket.recv()
            event = json.loads(message)
            
            # Ack request
            logging.info(f"\n------------------------------------------------------------------------------------")
            logging.info(f"Received request from {websocket.id}: {event}")
            self.add_client(websocket)

            assert event["type"] == "init"
            match event["action"]:
                case "lobby":
                    lobby = self._lobbies["default_lobby"]
                    await lobby.handle_lobby_requests(websocket)
        
                # case "join": pass
                
                case _: 
                    self.send_error(websocket, "unknown_error")

        finally:
            self.remove_client(websocket)



    # Send error messages to client
    async def send_error(self, websocket, message):
        try:
            event = {
                "type" : "error",
                "message" : message
            }

            await websocket.send(json.dumps(event))
        finally:
            logging.info("**Server initialization error")
            


    @property
    def lobby_list(self):
        return self.lobbies
    
    @property
    def chatroom_list(self):
        return self.chatroom
    
    # Connected clients properties
    @property
    def connect_client(self):
        return self._connected_clients
    
    def add_client(self, websocket):
        self._connected_clients.add(websocket)
        logging.info(f"++Added {websocket.id} from server")

    def remove_client(self, websocket):
        self._connected_clients.remove(websocket)
        logging.info(f"--Removed {websocket.id} from server")


    # Lobby properties
    @property
    def lobby_connected_clients(self):
        return self._lobbies
    
    def add_lobby(self, lobby_key, lobby_obj):
        self._lobbies[lobby_key] = lobby_obj

    def remove_lobby(self, lobby_key):
        self._lobbies.pop(lobby_key)
        
        

    @property
    def running_environment(self):
        if "chatroom-practice" in os.getcwd():
            return ENV_DEV
        else:
            return ENV_PROD