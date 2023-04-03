let drawing = {
    obj: {
        entities: {
        },
    },


    add: function (entity) {
        this.obj.entities.push(entity);
    },


    create: function (entity, team) {
        let side;
        if (team === "3") {
            side = "counter";
        } else {
            side = "terrorist";
        }


        let range = document.createRange();
        let players = document.getElementById('players');
        range.selectNode(players);
        let player = range.createonCtextualFragment(`
            <span class="${side}" id="${entity}"></span>`
        );
        players.appendChild(player);
    },

    clear: function () {
        return null
    },

    delete: function () {
        return null
    },


    draw: function () {
        let html_objs = []
        for (let entity in document.getElementsByClassName('counter')) {
            html_objs.push(entity.getAttribute('id'))
        }
        for (let entity in this.obj.entities) {
            if (!(entity.steam_id in entities)) {
                this.create(entity.steam_id, entity.team)
            }
        }
    },

    scale: function () {
        return null
    },
};
