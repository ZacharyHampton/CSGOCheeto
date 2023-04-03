function Drawing(players) {
    this.players = players;


    this.create = (entity, team, x, y) => {
        let players = document.getElementById('players')
        let player = document.createElement('div')
        player.id = entity
        switch (team) {
            case "3":
                player.className = "counter"
                break
            case "2":
                player.className = "terrorist"
                break
            default:
                return null;
        }
        player.style.left = -x + "px"
        player.style.top = -y + "px"
        players.appendChild(player)
    };


    this.update = (playerElement, x, y) => {
        playerElement.style.left = x + 'px';
        playerElement.style.top = y + 'px';
    }
}



const socket = new WebSocket("ws://127.0.0.1:8000/ws");
socket.onmessage = (event) => {
    let players = JSON.parse(event.data);
    players = JSON.parse(players);

    let drawing = new Drawing(players)

    for (let player of players.players) {
        let playerElement = document.getElementById(player.steam_id)

        let x = (parseInt(player.position.x) + 3230) / 6.4;
        let y = -(parseInt(player.position.y) - 1713) / 6.4;
        x = x.toString()
        y = y.toString()

        if (playerElement === null) {
            drawing.create(player.steam_id, player.team, x, y)
        } else {
            if (player.health > 0) {
                drawing.update(playerElement, x, y)
            } else {
                playerElement.remove()
            }

        }
    }
}





