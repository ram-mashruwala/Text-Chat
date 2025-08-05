const messages = document.querySelector(".messages")
const form = document.querySelector(".message-send");
const chat = document.querySelectorAll(".chat")
let username = ""
let socket = io()


socket.on("connect", (data) => {
	console.log("Connected on User end")
	socket.emit("requestUserName")
})

socket.on("message", (data) => {
	addMessage(data.author, data.message, false)
})

socket.on("addChat", (data) => {
	const chats = document.querySelector(".chat-list")
	chats.innerHTML += ` <div class="chat" onclick="joinChat(${data.chat_id})">
                <img src="../static/blankProfile.png" alt="Profile">
                <div class="chat-info">
                    <h2>${data.chat_name}</h2>
                </div>
            </div>`

})

socket.on("getUserName", (data) => {
	username = data.username
})

socket.on("getMessages", (data) => {
	for (let i = 0; i < data.text.length; i++) {
		let sent = false
		if (data.authors[i] === username) {
			sent = true
		}
		addMessage(data.authors[i], data.text[i], sent)
	}
})

socket.on("displayErrorMessage", (data) => {
	// Probably replace this with a splash screen of sorts
	console.error(data["message"])
})

form.addEventListener("submit", (e) => {
	e.preventDefault();
	const input = form[0];
	if (input.value != "") {
		socket.emit("message", {
			"message": input.value
		})
		addMessage(username, input.value, true)
		input.value = "";
	}
})


function joinChat(chatName) {
	socket.emit("joinChat", { "new_room": chatName })
	const chat = document.querySelector(".messages")
	chat.innerHTML = ""
}

function addMessage(author, text, sent) {
	if (sent) {
		messages.innerHTML += ` <div class='message sent'> <span>${author}</span> <p>${text}</p> </div>`
	} else {
		messages.innerHTML += ` <div class='message received'> <span>${author}</span> <p>${text}</p> </div>`
	}
	messages.scrollTop = messages.scrollHeight
}

function changeChatName(newName, id) {
	if (newName !== "") {
		socket.emit("changeChatName", { "new_chat_name": newName, "chat_id": id })
	}
}
