const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const chatMessage = document.getElementById('chat-message');
const recipientId = document.getElementById('recipient-id');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = document.createElement('div');
    message.textContent = `${data.sender} to ${data.recipient}: ${data.message}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

chatForm.onsubmit = function(e) {
    e.preventDefault();
    const message = chatMessage.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'recipient_id': recipientId.value
    }));
    chatMessage.value = '';
    return false;
};