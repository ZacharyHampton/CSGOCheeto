const socket = new WebSocket("127.0.0.1:8000/ws/asdf");

socket.onmessage = (info) => {
    var json_object = JSON.parse(info.data);

}

