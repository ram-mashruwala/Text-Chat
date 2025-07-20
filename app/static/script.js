const form = document.querySelector(".message-send");
let loggedIn = false
let socket = io()


socket.on("connect", (data) => {
	console.log("Connected on User end")
})

socket.on("message", (data) => {
	console.log(`${data.author}: ${data.message}`)
})

form.addEventListener("submit", (e) => {
	e.preventDefault();
	const input = form[0];
	if (loggedIn == false) {
		socket.emit("getUserName", { "username": input.value })
		loggedIn = true
	} else {
		socket.emit("message", {
			"message": input.value
		})
		console.log("You: " + input.value);
	}
	input.value = "";
})
