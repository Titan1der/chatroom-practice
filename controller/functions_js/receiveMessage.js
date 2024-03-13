import { hostRoom } from "./hostRoom.js";
import { joinRoom } from "./joinRoom.js";
import { updateChatLog } from "./updateChatLog.js";
import { updateRoomsList } from "./updateRoomsList.js";

export function receiveMessage(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const event = JSON.parse(data)

        switch(event.type) {
            case "host":
                console.log("Creating ROOM key");
                hostRoom(event.join)
                break;

            case "join":
                console.log("Creating JOIN and WATCH keys");
                joinRoom(event.userName)
                break;

            case "chat":
                console.log("Updating chat logs");
                updateChatLog(event.chatlog)
                break;

            case "rooms":
                console.log("Updating rooms list");
                updateRoomsList(event.roomList)
                break;

            default:
                console.log("Unsupported request");
                break;
        }
    });
}