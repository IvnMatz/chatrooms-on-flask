// static/chat.js

// Conectar al servidor WebSocket
const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
const chatID = document.getElementById('chatid');
const cID = chatID.innerText;

// Escuchar el evento de mensaje desde el servidor
socket.on('message', function(msg) {
    if (String(msg.channel) == String(cID)){
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.textContent = String(msg.username) + " : " + String(msg.message);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
    } // Auto scroll hacia el último mensaje
});

// Función para enviar el mensaje
function sendMessage() {
    const messageInput = document.getElementById("message");
    const msg = messageInput.value;
    socket.send({
        'msg' : msg,
        'channel' : cID
    })  // Enviar el mensaje al servidor
    messageInput.value = '';  // Limpiar el campo de entrada
}