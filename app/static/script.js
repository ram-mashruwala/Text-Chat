const form = document.querySelector(".message-send")

form.addEventListener("submit", (e) => {
	e.preventDefault()
	const input = form[0]
	console.log(input.value)
	input.value = ""
})


