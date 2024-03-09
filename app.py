import websockets
import asyncio
import os
import signal

from controller.functions_py.room_session_handler import handler
            
            
async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    # Uncomment before commit
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    

    port = int(os.environ.get("PORT", "8001"))
    
    async with websockets.serve(handler, "", port):
        print("Listening on websocket port:8001")
        await stop


if __name__ == "__main__":
    asyncio.run(main())
