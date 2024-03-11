import { initApp } from "./initApp.js";
import { receiveMessage } from "./receiveMessage.js";
import { sendMessage } from "./sendMessage.js";
import { getWebSocketServer } from "./getWebSocketServer.js"


window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer())

    initApp(websocket)
    receiveMessage(websocket)
    sendMessage(websocket)
});