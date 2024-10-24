const pin = document.getElementById("pin")
const phone = document.getElementById("phone")
const userName = document.getElementById("name")
const newPass = document.getElementById("new")
const reTypePass = document.getElementById("reType")
const signupForm = document.getElementById("signupForm")
const toastContainer = document.querySelector(".toast-container")
const toastCloseBtn = document.querySelector(".toast-close-btn")
let toastMessage = document.querySelector(".toast-message")


toastCloseBtn.onclick = () => {
    toastContainer.classList.toggle("active");
}

userName.addEventListener('keydown', (event) => {
    const allowedCharacters = /^[A-Za-z ]$/;
    const isControlKey = event.key === "Backspace" || event.key === "Tab" || event.key === "Delete" || event.key === "ArrowLeft" || event.key === "ArrowRight";
    if (!allowedCharacters.test(event.key) && !isControlKey) {
        event.preventDefault();
    }
    if (userName.value.length >= 50 && !isControlKey) {
        event.preventDefault();
    }
});

phone.addEventListener('keydown', (event) => {
    const isNumber = /^[0-9]$/;
    const isControlKey = event.key === "Backspace" || event.key === "Tab" || event.key === "Delete" || event.key === "ArrowLeft" || event.key === "ArrowRight";

    if (!isNumber.test(event.key) && !isControlKey) {
        event.preventDefault();
    }
    if (phone.value.length >= 10 && !isControlKey) {
        event.preventDefault();
    }
});

pin.addEventListener('keydown', (event) => {
    const isNumber = /^[0-9]$/;
    const isControlKey = event.key === "Backspace" || event.key === "Tab" || event.key === "Delete" || event.key === "ArrowLeft" || event.key === "ArrowRight";

    if (!isNumber.test(event.key) && !isControlKey) {
        event.preventDefault();
    }
    if (pin.value.length >= 6 && !isControlKey) {
        event.preventDefault();
    }
});


signupForm.onsubmit = () => {
    if (newPass.value != reTypePass.value) {
        toastContainer.classList.toggle("active");
        toastMessage.innerText = "The two new passwords must match";
        reTypePass.value = "";
        newPass.value = ""
        return (false);
    }
}