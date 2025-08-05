let selectedUsers = []
const userHolder = document.querySelector(".user-holder")
const form = document.querySelector(".inputer-form")
const secondForm = document.querySelector(".second-form")

form.addEventListener("submit", (e) => {
	e.preventDefault()
	const input = form[0]
	addUser(input.value)
	input.value = ""
})

secondForm.addEventListener("submit", (e) => {
	e.preventDefault()
	const nameInput = secondForm[0]
	let data = new FormData()
	data.append("name", nameInput.value)
	data.append("users", selectedUsers)
	fetch(`${SCRIPT_ROOT}${createChatURL}`, {
		"method": "POST",
		"body": data
	})
	console.log("Yipee???")
})

function addUser(username) {
	selectedUsers.push(username)
	addUserToSelectedUsers(username)
}

function addUserToSelectedUsers(username) {
	userHolder.innerHTML += `<div class='user-box'> <button onclick='deleteUser("${username}")'>X</button> <p>${username}</p> </div>`
}

function deleteUser(username) {
	console.log(username, selectedUsers)
	userHolder.innerHTML = ""
	let index = selectedUsers.indexOf(username)
	if (index > -1) {
		selectedUsers.splice(index, 1)
	}
	console.log(username, selectedUsers, index)

	for (let i = 0; i < selectedUsers.length; i++) {
		addUserToSelectedUsers(selectedUsers[i])
	}
}
