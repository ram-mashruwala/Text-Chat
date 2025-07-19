const form = document.querySelector(".message-send");
let socket = io()

form.addEventListener("submit", (e) => {
	e.preventDefault();
	const input = form[0];
	console.log(input.value);
	input.value = "";
})

socket.on("connect", (data) => {
	console.log("Connected on User end")
})
