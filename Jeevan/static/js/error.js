let errorMsg = document.querySelector(".error-message");
let errorBtn = document.querySelector(".error-btn");

errorBtn.onclick = () => {
  
    if (errorMsg.style.display === "block") {
      errorMsg.style.display = "none";
      errorBtn.innerHTML = "View details";

    } else {
      errorMsg.style.display = "block";
      errorBtn.innerHTML = "Close details";
    }
}