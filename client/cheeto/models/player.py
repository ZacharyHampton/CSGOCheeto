from pydantic import BaseModel
from client.internal.objects.vector3 import Vector3


class Player(BaseModel):
    steam_id: str
    name: str
    team: str
    health: int
    position: Vector3
    weapon_id: int
    isLocalPlayer: bool
