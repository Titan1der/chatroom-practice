function sendMessageHandler(websocket) {
    const inputText = document.querySelector("#input-txt").value

        const event = { 
            type : "chat",
            text :  inputText
        }

        document.querySelector("#input-txt").value = ""
        websocket.send(JSON.stringify(event))
}


export function sendMessage(websocket) {
    const sendButton = document.querySelector("#send-btn")
    const inputText = document.querySelector("#input-txt")

    sendButton.addEventListener("click", () => { sendMessageHandler(websocket) });
    inputText.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { sendMessageHandler(websocket) }
    });
}