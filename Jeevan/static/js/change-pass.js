const currentPass = document.getElementById("current")
const newPass = document.getElementById("new")
const reTypePass = document.getElementById("reType")
const changePassForm = document.getElementById("changePassForm")
const toastContainer = document.querySelector(".toast-container")
const toastCloseBtn = document.querySelector(".toast-close-btn")
let toastMessage = document.querySelector(".toast-message")

toastCloseBtn.onclick = () => {
    toastContainer.classList.toggle("active");
}

changePassForm.onsubmit = () => {
    // check if password fields are empty
    if(newPass.value != reTypePass.value) 
    {
        toastContainer.classList.toggle("active");
        toastMessage.innerText = "The two new passwords must match";
        reTypePass.value = "";
        newPass.value = ""
        return (false);
    }
}