import pymem
import memprocfs
import time
import struct
import memprocfs.vmmpyc
from client.internal.memwrapper.file_conversion import TypeConversion
from client.internal.memwrapper.exceptions import NullPointerError, MissingRequiredFieldError
import ctypes
import _ctypes
from ctypes import c_uint32


class Memory:
    def __init__(self):
        try:
            self.vmm = memprocfs.Vmm(["-printf", "-device", "FPGA", "-memmap", "auto"])
            self.dma = True
        except TypeError:
            self.dma = False

        self.process = self.get_process()

    def get_process(self) -> pymem.Pymem | memprocfs.vmmpyc.VmmProcess:
        while True:
            try:
                if self.dma:
                    return self.vmm.process('csgo.exe')
                else:
                    return pymem.Pymem('csgo.exe')
            except (RuntimeError, pymem.exception.ProcessNotFound):
                time.sleep(1)

    def read(self, address: int, datatype: type(_ctypes._SimpleCData)) -> TypeConversion:
        size = ctypes.sizeof(datatype)

        if self.dma:
            return TypeConversion(self.process.memory.read(address, size, memprocfs.FLAG_NOCACHE))
        else:
            return TypeConversion(self.process.read_bytes(address, size))

    def read_ptr(self, address: int, ignore_null: bool = False):
        #: CS:GO uses 32-bit pointers

        if (pointer := int(self.read(address, datatype=c_uint32))) != 0x0:
            return pointer
        elif ignore_null:
            return 0x0
        else:
            raise NullPointerError(f"Null pointer at address {hex(address)} with a value of {hex(pointer)}")

    def read_ptr_chain(self, pointer: int, offsets: list[int]):
        address: int = self.read_ptr(pointer + offsets[0])
        for offset in offsets[1:]:
            address = self.read_ptr(address + offset)

        return address

    def module_from_name(self, module_name: str):
        while True:
            try:
                if self.dma:
                    return self.process.module(module_name).base
                else:
                    return pymem.process.module_from_name(self.process.process_handle, module_name).lpBaseOfDll
            except (AttributeError, RuntimeError):
                time.sleep(1)
                continue

