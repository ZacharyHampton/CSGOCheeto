from client.cheeto.globals import memory, offsets
from ctypes import c_uint32, c_int8
from client.cheeto.objects.entity import Entity


class Engine:
    def __init__(self):
        self.clientState = memory.read_ptr(offsets.engine + offsets.dwClientState)

    def get_local_player(self):
        localPlayerIndex = memory.read_ptr(self.clientState + offsets.dwClientState_GetLocalPlayer, ignore_null=True)
        return Entity.get_client_entity(localPlayerIndex)

    """@staticmethod
    def get_view_angles():
        return mem.read_vec3(nv.dwClientState + nv.dwViewAngles)"""

    def get_max_clients(self):
        return memory.read_ptr(self.clientState + offsets.dwClientState_MaxPlayer)

    def is_in_game(self):
        return int(memory.read(self.clientState + offsets.dwClientState_State, c_int8)) >> 2
