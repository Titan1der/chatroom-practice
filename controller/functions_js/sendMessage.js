function sendMessageHandler(websocket) {
    const inputText = document.querySelector("#input-text").value

        const event = { 
            type : "chat",
            request : "sendMessage",
            text :  inputText
        }

        document.querySelector("#input-text").value = ""
        websocket.send(JSON.stringify(event))
}


export function sendMessage(websocket) {
    const sendButton = document.querySelector("#send-btn")
    const inputText = document.querySelector("#input-text")

    // sendButton.addEventListener("click", () => { sendMessageHandler(websocket) });
    inputText.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) { sendMessageHandler(websocket) }
    });
}