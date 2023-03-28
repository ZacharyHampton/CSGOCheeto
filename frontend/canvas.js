function info() {
    const socket = new WebSocket("127.0.0.1:8000/ws/asdf");
    socket.onmessage = (event) => {
        let json_object = JSON.parse(event.data);
        alert('it worked');
    }
}

var GameArea = {
    canvas: document.createElement("canvas"),
    start: function() {
      this.canvas.width = 1024;
      this.canvas.height = 1024;
      this.context = this.canvas.getContext("2d");
      document.body.insertBefore(this.canvas, null);
    }
}
function component(width, height, color, x, y) {
    this.width = width;
    this.height = height;
    this.x = x;
    this.y = y;
    ctx = myGameArea.context;
    ctx.fillStyle = color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
}