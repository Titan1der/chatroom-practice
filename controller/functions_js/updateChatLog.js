export function updateChatLog(chatLog) {
    // Update the chatbox with latest message
    const ulistMessages = document.querySelector("#list-messages")
    const lastMsg = chatLog[chatLog.length - 1];
    ulistMessages.innerHTML += `<li class='chat-message'>${lastMsg}</li>`

    // Keep the scrollbar scrolled down\
    ulistMessages.lastChild.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
}