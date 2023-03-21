import pymem
import memprocfs
import time
import struct


class Memory:
    def __init__(self):

        try:
            self.vmm = memprocfs.Vmm(["-printf", "-device", "FPGA", "-memmap", "auto"])
            self.dma = True
        except TypeError as e:
            self.dma = False

        self.process = self.get_process()

    def get_process(self):
        while True:
            try:
                if self.dma:
                    return self.vmm.process('csgo.exe')
                else:
                    return pymem.Pymem('csgo.exe')
            except (RuntimeError, pymem.exception.ProcessNotFound):
                time.sleep(1)

    def read(self, address: int, size: int):
        if self.dma:
            return self.process.memory.read(address, size, memprocfs.FLAG_NOCACHE)
        else:
            return self.process.read_bytes(address, size)

    def read_ptr(self, address: int):
        return int.from_bytes(self.read(address, struct.calcsize("LL")), 'little')
