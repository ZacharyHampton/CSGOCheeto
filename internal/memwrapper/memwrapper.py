import pymem
import memprocfs


class Memory:
    def __init__(self):
        try:
            self.vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
        except TypeError as e:
            if "vmm failed" in str(e):
                self.dma = False

        self.dma = True
