const form = document.querySelector(".message-send");
let loggedIn = false
let socket = io()


socket.on("connect", (data) => {
	console.log("Connected on User end")
	// Once we figure out the settings we should add a socket.emit that requests all previous messages in current room and all user settings
})

socket.on("message", (data) => {
	document.querySelector(".messages").innerHTML += ` <div class='message received'> <span>${data.author}</span> <p>${data.message}</p> </div>`
})

form.addEventListener("submit", (e) => {
	e.preventDefault();
	const input = form[0];
	// Probably remove the login thingy once we get login page to work
	if (loggedIn == false) {
		socket.emit("getUserName", { "username": input.value })
		loggedIn = true
	} else {
		socket.emit("message", {
			"message": input.value
		})
		document.querySelector(".messages").innerHTML += ` <div class='message sent'> <span>YOU</span> <p>${input.value}</p> </div>`
	}
	input.value = "";
})
