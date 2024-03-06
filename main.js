function initApp(websocket) {
    websocket.addEventListener("open", () => {
        let event = { type : "init" }
        const params = new URLSearchParams(window.location.search)

        if (params.has("join")) {
            event.action = "join"
        }
        else if (params.has("watch")) {
            event.action = "watch"
        }
        else {
            event.action = "host"
        }

        websocket.send(JSON.stringify(event))
    });
}


function hostRoom(joinKey, watchKey) {
    document.querySelector("#joinLink").href = "?join=" + joinKey
    document.querySelector("#joinLink").style.visibility = "visible"

    document.querySelector("#watchLink").href = "?watch=" + watchKey
    document.querySelector("#watchLink").style.visibility = "visible"
}


function receiveMessage(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data)

        switch(event.type) {
            case "host":
                console.log("Creating JOIN and WATCH keys");
                hostRoom(event.join, event.watch)
        }
    });
}


window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001")
    initApp(websocket)
    receiveMessage(websocket)
});