// get roomName, or connection_id in this case to know who's talking to who, and username
var boxName = JSON.parse(document.getElementById('room-name').textContent);
var user_username = JSON.parse(document.getElementById('user_username').textContent);

try{
    chatSocket.close();
    // delete chatSocket;
}
catch{

}

// Create a WebSocket in JavaScript.
var chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    boxName +
    '/'
);

// send message and other info to backend (consumers.py through routing.py)
// document.querySelector('#submit').onclick = function (e) {
//     const messageInputDom = document.querySelector('#input');
//     const message = messageInputDom.value;
//     chatSocket.send(JSON.stringify({
//         'message': message,
//         'username': user_username,
//         'connection_id': boxName,
//     }));
//     messageInputDom.value = '';
// };


// once message is processed and recieved from backend, display inside textarea
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // document.querySelector('#chat-text').value += (data.message + ' sent by ' + data.username   + '\n')
    
    // add message to text box

    addMessagestoChatBox(data);
}

// submit on pressing enter
document.querySelector("#input").focus();
document.querySelector("#input").onkeyup = function (e) {
    if (e.keyCode === 13) {
    // enter, return
    // send message and other info to backend (consumers.py through routing.py)
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': user_username,
        'connection_id': boxName,
    }));
    messageInputDom.value = '';
    }
};
