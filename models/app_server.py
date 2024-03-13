import os
import websockets
import json

from controller.functions_py.constants import *
from websockets import WebSocketServerProtocol

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class AppServer(object):
    def __init__(self):
        self._lobbies = set()
        self._chatroom = set()
        self._connected_clients = set()

        logging.info("App server started")

    async def handle_requests(self, websocket : WebSocketServerProtocol):
        try:
            message = await websocket.recv()
            event = json.loads(message)
            
            # Ack request
            logging.info(f"Received request from {websocket.id}: {event}")
            self.add_client(websocket)

            assert event["type"] == "init"

            match event["action"]:
                case "lobby": pass
                case "join": pass
                case _: 
                    self.send_error(websocket, "unknown_error")

        finally:
            self.remove_client(websocket)
            logging.info(f"**Removed {websocket.id}")


    @property
    def lobby_list(self):
        return self.lobbies
    
    @property
    def chatroom_list(self):
        return self.chatroom
    
    @property
    def connect_client(self):
        return self._connected_clients
    
    def add_client(self, websocket):
        self._connected_clients.add(websocket)

    def remove_client(self, websocket):
        self._connected_clients.remove(websocket)

    @property
    def running_environment(self):
        if "chatroom-practice" in os.getcwd():
            return ENV_DEV
        else:
            return ENV_PROD
        

    async def send_error(self, websocket, message):
        try:
            event = {
                "type" : "error",
                "message" : message
            }

            await websocket.send(json.dumps(event))
        finally:
            logging.info("**Server initialization error")