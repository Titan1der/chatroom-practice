function initStartup(websocket) {
    let event = { type : "init" }
        const params = new URLSearchParams(window.location.search)
        document.querySelector("#input-text").placeholder = "Write your message here..."

        if (params.has("host")) {
            event.action = "host"
            event.key= params.get("host")
        }
        
        else if (params.has("join")) {
            event.action = "join"
            event.key= params.get("join")
        }

        else if (params.has("watch")) {
            event.action = "watch"
            event.key = params.get("watch")
        }

        else {
            event.action = "host"
        }

        websocket.send(JSON.stringify(event))
}

export function initApp(websocket) {
    websocket.addEventListener("open", () => {
        initStartup(websocket)
    });

    // Websocket closed cases
    websocket.addEventListener("closed", () => {
        document.querySelector("#input-text").placeholder = "Closed: Could not connect to websocket."
    });

    websocket.addEventListener("error", () => {
        document.querySelector("#input-text").placeholder = "Error: Could not connect to websocket."
    });

    if (websocket.readyState === WebSocket.CLOSED) {
        document.querySelector("#input-text").placeholder = "Websocket closed."
    }
}