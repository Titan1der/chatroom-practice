export function updateChatLog(chatLog) {
    let res = ""
    chatLog.forEach(line => {
        res += line + "<br>"
    });

    document.querySelector("#chatbox").innerHTML = res
}