const form = document.querySelector(".message-send");
const chat = document.querySelectorAll(".chat")
let username = ""
let socket = io()


socket.on("connect", (data) => {
	console.log("Connected on User end")
	socket.emit("requestUserName")
})

socket.on("message", (data) => {
	const chat = document.querySelector(".messages")
	chat.innerHTML += ` <div class='message received'> <span>${data.author}</span> <p>${data.message}</p> </div>`
	chat.scrollTop = chat.scrollHeight
})

socket.on("addChat", (data) => {
	const chats = document.querySelector(".chat-list")
	chats.innerHTML += ` <div class="chat">
                <img src="../static/blankProfile.png" alt="Profile">
                <div class="chat-info">
                    <h2>${data["username"]}</h2>
                </div>
            </div>`

})

socket.on("getUserName", (data) => {
	username = data["username"]
})

form.addEventListener("submit", (e) => {
	const chat = document.querySelector(".messages")
	e.preventDefault();
	const input = form[0];
	if (input.value != "") {
		socket.emit("message", {
			"message": input.value
		})
		chat.innerHTML += ` <div class='message sent'> <span>${username}</span> <p>${input.value}</p> </div>`
		input.value = "";
		chat.scrollTop = chat.scrollHeight
	}
})


function joinChat(chatName) {
	socket.emit("joinChat", { "new_room": chatName })
	const chat = document.querySelector(".messages")
	chat.innerHTML = ""
}


