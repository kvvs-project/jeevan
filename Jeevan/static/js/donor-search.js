var typeRadio = document.getElementsByName("type");

if (typeof(typeRadio) != 'undefined' && typeRadio != null){
    var bloodRadio = document.getElementById("blood");
    var organList = document.getElementById("organ-search");
    var organSelectNull = document.getElementById("organ-list-default");

    typeRadio.forEach((item) => {
        item.addEventListener("click", () => {
            organList.style.display =  "none";                          // handle an edge case where if user
            if (bloodRadio.checked) {                                   // selects a organ name before choosing  
                organSelectNull.setAttribute("selected", "selected");   // the donation type the selected 
            } else {                                                    // organ is sent to backend
                organList.style.display =  "flex";
            }
        })
    });
}