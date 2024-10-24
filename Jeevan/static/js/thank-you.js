const copyButton = document.querySelector(".copy-btn");
const userID = document.querySelector(".user-id");

copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(userID.innerText) 
});