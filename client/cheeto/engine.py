from client.internal.memory import Memory
class Player:
    def __init__(self, address):
        self.address = address

    def get_team_num(self):
        return mem.read_i32(self.address + nv.m_iTeamNum)

    def get_health(self):
        return mem.read_i32(self.address + nv.m_iHealth)

    def get_life_state(self):
        return mem.read_i32(self.address + nv.m_lifeState)

    def get_tick_count(self):
        return mem.read_i32(self.address + nv.m_nTickBase)

    def get_shots_fired(self):
        return mem.read_i32(self.address + nv.m_iShotsFired)

    def get_cross_index(self):
        return mem.read_i32(self.address + nv.m_iCrossHairID)

    def get_weapon(self):
        a0 = mem.read_i32(self.address + nv.m_hActiveWeapon)
        return mem.read_i32(nv.dwEntityList + ((a0 & 0xFFF) - 1) * 0x10)

    def get_weapon_id(self):
        return mem.read_i32(self.get_weapon() + nv.m_iItemDefinitionIndex)

    def get_origin(self):
        return mem.read_vec3(self.address + nv.m_vecOrigin)

    def get_vec_view(self):
        return mem.read_vec3(self.address + nv.m_vecViewOffset)

    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_origin()
        return Vector3(v.x + o.x, v.y + o.y, v.z + o.z)

    def get_vec_punch(self):
        return mem.read_vec3(self.address + nv.m_vecPunch)

    def get_bone_pos(self, index):
        a0 = 0x30 * index
        a1 = mem.read_i32(self.address + nv.m_dwBoneMatrix)
        return Vector3(
            mem.read_float(a1 + a0 + 0x0C),
            mem.read_float(a1 + a0 + 0x1C),
            mem.read_float(a1 + a0 + 0x2C)
        )