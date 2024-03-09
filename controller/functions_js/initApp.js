export function initApp(websocket) {
    websocket.addEventListener("open", () => {
        let event = { type : "init" }
        const params = new URLSearchParams(window.location.search)

        if (params.has("join")) {
            event.action = "join"

            const joinKey = params.get("join")
            event.key = joinKey
        }
        else if (params.has("watch")) {
            event.action = "watch"

            const watchKey = params.get("watch")
            event.key = watchKey
        }
        else {
            event.action = "host"
        }

        websocket.send(JSON.stringify(event))
    });

    // Websocket closed cases
    websocket.addEventListener("closed", () => {
        document.querySelector("#websocketState").style.display = "block"
        document.querySelector("#websocketState").style.visibility = "visible"
    });

    websocket.addEventListener("error", () => {
        document.querySelector("#websocketState").style.display = "block"
        document.querySelector("#websocketState").style.visibility = "visible"
    });

    if (websocket.readyState === WebSocket.CLOSED) {
        document.querySelector("#websocketState").style.display = "block"
        document.querySelector("#websocketState").style.visibility = "visible"
    }
}