from client.cheeto.objects.player import Player
from client.cheeto.globals import memory, offsets


class Entity:
    @staticmethod
    def get_client_entity(index):
        return Player(memory.read_ptr(offsets.dwEntityList + index * 0x10))
