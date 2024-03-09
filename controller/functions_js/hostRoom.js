export function hostRoom(joinKey, watchKey) {
    document.querySelector("#websocketState").style.display = "none"
    document.querySelector("#websocketState").style.visibility = "hidden"
    document.querySelector("#joinLink").href = "?join=" + joinKey
    document.querySelector("#joinLink").style.display = "block"
    document.querySelector("#joinLink").style.visibility = "visible"
    document.querySelector("#watchLink").href = "?watch=" + watchKey
    document.querySelector("#watchLink").style.display = "block"
    document.querySelector("#watchLink").style.visibility = "visible"
}