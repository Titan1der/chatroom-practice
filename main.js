function initApp(websocket) {
    websocket.addEventListener("open", () => {
        let event = { type : "init" }
        const params = new URLSearchParams(window.location.search)

        if (params.has("join")) {
            event.action = "join"

            joinKey = params.get("join")
            event.key = joinKey
        }
        else if (params.has("watch")) {
            event.action = "watch"

            watchKey = params.get("watch")
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


function hostRoom(joinKey, watchKey) {
    document.querySelector("#websocketState").style.display = "none"
    document.querySelector("#websocketState").style.visibility = "hidden"
    document.querySelector("#joinLink").href = "?join=" + joinKey
    document.querySelector("#joinLink").style.display = "block"
    document.querySelector("#joinLink").style.visibility = "visible"
    document.querySelector("#watchLink").href = "?watch=" + watchKey
    document.querySelector("#watchLink").style.display = "block"
    document.querySelector("#watchLink").style.visibility = "visible"
}


function updateChatLog(chatLog) {
    let res = ""
    chatLog.forEach(line => {
        res += line + "<br>"
    });

    document.querySelector("#chatbox").innerHTML = res
}


function joinRoom(name) {
    document.querySelector("#websocketState").style.display = "none"
    document.querySelector("#websocketState").style.visibility = "hidden"
    document.querySelector("#joinLink").style.display = "none"
    document.querySelector("#joinLink").style.visibility = "hidden"
    document.querySelector("#watchLink").style.display = "none"
    document.querySelector("#watchLink").style.visibility = "hidden"
}


function receiveMessage(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data)

        switch(event.type) {
            case "host":
                console.log("Creating JOIN and WATCH keys");
                hostRoom(event.join, event.watch)
                break;

            case "join":
                console.log("Creating JOIN and WATCH keys");
                joinRoom(event.userName)
                break;

            case "chat":
                console.log("Updating chat logs");
                updateChatLog(event.chatlog)
                break;

            default:
                console.log("Unsupported request");
                break;
        }
    });
}


function sendMessageHandler(websocket) {
    const inputText = document.querySelector("#input-txt").value

        const event = { 
            type : "chat",
            text :  inputText
        }

        document.querySelector("#input-txt").value = ""
        websocket.send(JSON.stringify(event))
}


function sendMessage(websocket) {
    const sendButton = document.querySelector("#send-btn")
    const inputText = document.querySelector("#input-txt")

    sendButton.addEventListener("click", () => { sendMessageHandler(websocket) });
    inputText.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { sendMessageHandler(websocket) }
    });
}


function getWebSocketServer() {
    if (window.location.host === "Titan1der.github.io") {
        return "wss://websocket-chatroom-test-0081e647aa7f.herokuapp.com/";
    }
    else if (window.location.host === "localhost:5500") {
        return "ws://localhost:8001";
    }
    else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}


window.addEventListener("DOMContentLoaded", () => {
    const websocket = getWebSocketServer()

    initApp(websocket)
    receiveMessage(websocket)
    sendMessage(websocket)
});