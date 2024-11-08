const user = document.getElementById("AddUser");
const chat = document.getElementById("chat");

//buttons
const c = document.getElementById("c");
const au = document.getElementById("au");

function showU(){
    user.style.display="block";
    chat.style.display="none";
}

function showC(){
    user.style.display="none";
    chat.style.display="block";
}

c.onclick=showC;
au.onclick=showU;