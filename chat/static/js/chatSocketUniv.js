// Create a WebSocket in JavaScript.
var chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/'
);


// on msg, add it status of users on left side. refresh later for order by latest message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    addMessagestoStatus(data);
}


function addMessagestoStatus(data){
    console.log("thissss");
    document.getElementById("connection_status-" + data.connection_id).innerHTML = " <i class='fa fa-circle online'></i> " + data.message + " ";
}