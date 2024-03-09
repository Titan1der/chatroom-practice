import { initApp } from "./controller/functions_js/initApp.js";
import { receiveMessage } from "./controller/functions_js/receiveMessage.js";
import { sendMessage } from "./controller/functions_js/sendMessage.js";
import { getWebSocketServer } from "./controller/functions_js/getWebSocketServer.js";


window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket(getWebSocketServer())

    initApp(websocket)
    receiveMessage(websocket)
    sendMessage(websocket)
});