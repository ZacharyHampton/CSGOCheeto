function Drawing(players) {
    this.players = players;


    this.create = (entity, team) => {
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
        players.appendChild(player)
    };


    this.update = (playerElement, x, y, team) => {
        let position = this.scale(x, y)
        playerElement.style.left = position.x + 'px';
        playerElement.style.top = position.y + 'px';
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


    this.scale = (x, y) => {
        let maps = {'de_dust2.png':[-2476,3239,4.4] ,'de_inferno.png': [-2087,3870,4.9], 'de_vertigo.png':[-3168,1762,4], 'de_nuke.png': [-3453, 2887, 7], 'de_mirage.png':[-3230, 1713, 5]}
        let imgheight = document.getElementById("map-img").height
        let map = document.getElementById("map-img").src.match(/([^\/]*)\/*$/)[1]
        let offsetx = maps[map][0]
        let offsety = maps[map][1]
        let gameScale = maps[map][2]
        let xpos = (((parseInt(x)) - offsetx) * imgheight) / (gameScale*1024).toString();
        let ypos = -(((parseInt(y)) - offsety) * imgheight) / (gameScale*1024).toString();
        return {"x": xpos, "y": ypos}
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

    if (data.status === "game_started") {
         let a = data.map.name
         document.getElementById('map-img').src = a + ".png"
    }

    for (let player of data.players) {

        if (player.health > 0) {
            let playerElement = document.getElementById(player.steam_id)
            let y = player.position.y
            if (playerElement === null) {
                drawing.create(player.steam_id, player.team)
            } else {
                drawing.update(playerElement, player.position.x, y, player.team)
            }
        } else {
            document.getElementById(player.steam_id).remove()
        }
    }
}





