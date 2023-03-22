from client.cheeto.globals import memory, offsets
from ctypes import c_float, c_int32
from client.internal.objects.vector3 import Vector3


class Player:
    def __init__(self, address):
        self.address = address

    def get_team_num(self):
        return memory.read_ptr(self.address + offsets.m_iTeamNum)

    def get_health(self):
        return int(memory.read(self.address + offsets.m_iHealth, c_int32))

    def get_life_state(self):
        return memory.read_ptr(self.address + offsets.m_lifeState)

    def get_tick_count(self):
        return memory.read_ptr(self.address + offsets.m_nTickBase)

    def get_shots_fired(self):
        return memory.read_ptr(self.address + offsets.m_iShotsFired)

    def get_weapon(self):
        a0 = memory.read_ptr(self.address + offsets.m_hActiveWeapon)
        return memory.read_ptr(offsets.dwEntityList + ((a0 & 0xFFF) - 1) * 0x10)

    def get_weapon_id(self):
        return memory.read_ptr(self.get_weapon() + offsets.m_iItemDefinitionIndex)

    """def get_origin(self):
        return mem.read_vec3(self.address + offsets.m_vecOrigin)

    def get_vec_view(self):
        return mem.read_vec3(self.address + offsets.m_vecViewOffset)

    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_origin()
        return Vector3(v.x + o.x, v.y + o.y, v.z + o.z)"""

    def get_bone_pos(self, index):
        a0 = 0x30 * index
        a1 = memory.read_ptr(self.address + offsets.m_dwBoneMatrix)
        return Vector3(
            float(memory.read(a1 + a0 + 0x0C, c_float)),
            float(memory.read(a1 + a0 + 0x1C, c_float)),
            float(memory.read(a1 + a0 + 0x2C, c_float))
        )