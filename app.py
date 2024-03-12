import websockets
import asyncio
import os
import signal

from controller.functions_py.constants import *
from models.app_server import AppServer
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


async def main():
    app = AppServer()

    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    if app.running_environment == ENV_PROD:
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    
    port = int(os.environ.get("PORT", "8001"))
    
    async with websockets.serve(app.handle_requests, "", port):
        logging.info("Listening on websocket port:8001")
        await stop


if __name__ == "__main__":
    asyncio.run(main())
    
    