from pydantic import BaseModel
from client.cheeto.models.player import Player
from client.cheeto.models.map import Map
from client.cheeto.models.status import Status
from typing import List


class Packet(BaseModel):
    players: List[Player] = []
    map: Map = None
    status: Status
