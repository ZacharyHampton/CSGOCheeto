class TypeConversion:
    def __init__(self, conversion_bytes: bytes):
        self.bytes = conversion_bytes
        self.int = int.from_bytes(conversion_bytes, 'little')

