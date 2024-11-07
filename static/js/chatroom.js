const chats = document.getElementById("ChatList");
const changeColor = document.getElementById("changeC");
const Cchat = document.getElementById("chatForm");

//buttons
const bc = document.getElementById("bc");
const bcc = document.getElementById("bcc");
const bcuc = document.getElementById("bcuc");

function ShowChats(){
    chats.style.display="block";
    changeColor.style.display="none";
    Cchat.style.display="none";
}
function ShowChange(){
    chats.style.display="none";
    changeColor.style.display="block";
    Cchat.style.display="none";
}
function ShowCchat(){
    chats.style.display="none";
    changeColor.style.display="none";
    Cchat.style.display="block";
}

bc.onclick=ShowChats;
bcuc.onclick=ShowChange;
bcc.onclick=ShowCchat;