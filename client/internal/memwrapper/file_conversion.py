import struct


class TypeConversion:
    def __init__(self, conversion_bytes: bytes):
        self.bytes = conversion_bytes

    def __int__(self):
        return int.from_bytes(self.bytes, 'little')

    def __float__(self):
        try:
            return struct.unpack('f', self.bytes)[0]
        except struct.error:
            return 0.0

    def __str__(self):
        return self.bytes.decode('utf-8').split('\x00')[0]
