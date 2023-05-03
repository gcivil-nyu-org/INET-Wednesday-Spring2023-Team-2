// Create a WebSocket in JavaScript.
var chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/'
);


// on msg, add it status of users on left side. refresh later for order by latest message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("here?");
    try{
        addMessagestoStatus(data);
    }
    catch{
        updateUserPendingStatus();
    }
    // addMessageNotification();
}