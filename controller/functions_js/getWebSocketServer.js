export function getWebSocketServer() {
    if (window.location.host === "titan1der.github.io") {
        return "wss://websocket-chatroom-test-0081e647aa7f.herokuapp.com/";
    }
    else if (window.location.host === "localhost:5500" || window.location.host === "127.0.0.1:5500") {
        return "ws://localhost:8001";
    }
    else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}