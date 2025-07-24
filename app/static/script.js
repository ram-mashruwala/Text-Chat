const form = document.querySelector(".message-send");
let socket = io()


socket.on("connect", (data) => {
	console.log("Connected on User end")
	// Once we figure out the settings we should add a socket.emit that requests all previous messages in current room and all user settings
})

socket.on("message", (data) => {
	const chat = document.querySelector(".messages")
	chat.innerHTML += ` <div class='message received'> <span>${data.author}</span> <p>${data.message}</p> </div>`
	chat.scrollTop = chat.scrollHeight
})

form.addEventListener("submit", (e) => {
	const chat = document.querySelector(".messages")
	e.preventDefault();
	const input = form[0];
	if (input.value != "") {
		socket.emit("message", {
			"message": input.value
		})
		chat.innerHTML += ` <div class='message sent'> <span>YOU</span> <p>${input.value}</p> </div>`
		input.value = "";
		chat.scrollTop = chat.scrollHeight
	}
})
