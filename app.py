import websockets
import asyncio
import os
import signal

from controller.functions_py.constants import *

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

from controller.functions_py.room_session_handler import handler
            

def get_working_environment():
    if "chatroom-practice" in os.getcwd():
        return ENV_DEV
    else:
        return ENV_PROD
    
            
async def main():
    # Current environment
    environment = get_working_environment()
    logging.info(f"Current environment: {environment}")
    
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    if environment == ENV_PROD:
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    
    port = int(os.environ.get("PORT", "8001"))
    
    async with websockets.serve(handler, "", port):
        logging.info("Listening on websocket port:8001")
        await stop


if __name__ == "__main__":
    asyncio.run(main())
