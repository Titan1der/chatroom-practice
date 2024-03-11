export function updateRoomsList(rooms) {
    const roomList = document.querySelector("#list-rooms")
    roomList.innerHTML = ""

    let numOfRooms = Object.keys(rooms).length

    if (numOfRooms == 0) {
        roomList.innerHTML = '<li class="empty-rooms">No Rooms Available</li>'
    }

    else {
        for (const [key, value] of Object.entries(rooms)) {
            console.log(`Key: ${key}, Value: ${value}`);
            roomList.innerHTML += `<li class="open-room">Room#${key}: ${value}</li>`
        }
    }
}


