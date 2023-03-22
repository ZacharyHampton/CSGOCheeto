from client.cheeto.globals import memory, offsets
from ctypes import c_uint32, c_int8


class Engine:
    def __init__(self, engine_ptr: int):
        self.engine_ptr = engine_ptr

    def get_local_player(self):
        return memory.read_ptr(self.engine_ptr + offsets.dwClientState_GetLocalPlayer, ignore_null=True)

    """@staticmethod
    def get_view_angles():
        return mem.read_vec3(nv.dwClientState + nv.dwViewAngles)"""

    def get_max_clients(self):
        return memory.read_ptr(self.engine_ptr + offsets.dwClientState_MaxPlayer)

    def is_in_game(self):
        return int(memory.read(self.engine_ptr + offsets.dwClientState_State, c_int8)) >> 2
