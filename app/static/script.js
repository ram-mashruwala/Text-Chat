const form = document.querySelector(".message-send");
const chat = document.querySelectorAll(".chat")
console.log(chat)
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

socket.on("addChat", (data) => {
	const chats = document.querySelector(".chat-list")
	chats.innerHTML += ` <div class="chat">
                <img src="../static/blankProfile.png" alt="Profile">
                <div class="chat-info">
                    <h2>${data["username"]}</h2>
                </div>
            </div>`

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


