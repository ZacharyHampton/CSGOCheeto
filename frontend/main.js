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


    this.update = (playerElement, x, y, team) => {
        playerElement.style.left = x + 'px';
        playerElement.style.top = y + 'px';
        switch (team) {
            case "3":
                playerElement.className = "counter"
                break
            case "2":
                playerElement.className = "terrorist"
                break
            default:
                return null;
        }
    }


    this.clear = (className) => {
        let elements = document.getELementsByClassName(className)
        for (let element in elements) {
            element.remove()
        }
    }
}



const socket = new WebSocket("ws://127.0.0.1:8000/ws");
socket.onmessage = (event) => {
    let data = JSON.parse(event.data);
    data = JSON.parse(data);

    let drawing = new Drawing(data)

    if (data.status === "game_ended") {
        drawing.clear("terrorist")
        drawing.clear("counter")
    }


    for (let player of data.players) {
        let playerElement = document.getElementById(player.steam_id)

        let x = (parseInt(player.position.x) + 2087) / 6.3;
        let y = -(parseInt(player.position.y) - 3870) / 6.3;
        x = x.toString()
        y = y.toString()

        if (playerElement === null) {
            drawing.create(player.steam_id, player.team, x, y)
        } else {
            if (player.health > 0) {
                drawing.update(playerElement, x, y, player.team)
            } else {
                playerElement.remove()
            }

        }
    }
}





