import struct
from io import BufferedWriter, DEFAULT_BUFFER_SIZE
from uuid import UUID

class DataWriter():
    def __init__(self, writer, buffer_size=DEFAULT_BUFFER_SIZE):
        self.writer = writer

    def write(self, b):
        self.writer.write(b)

    def flush(self):
        self.writer.flush()

    def write_boolean(self, value):
        if not isinstance(bool, value):
            value = bool(value)
        self.write(struct.pack('>B', value))

    def write_sbyte(self, value):
        self.write(struct.pack('>b', value))

    def write_byte(self, value):
        self.write(struct.pack('>B', value))

    def write_short(self, value):
        self.write(struct.pack('>h', value))

    def write_ushort(self, value):
        self.write(struct.pack('>H', value))

    def write_int(self, value):
        self.write(struct.pack('>i', value))

    def write_long(self, value):
        self.write(struct.pack('>q', value))

    def write_float(self, value):
        self.write(struct.pack('>f', value))

    def write_double(self, value):
        self.write(struct.pack('>d', value))

    def write_string(self, value):
        encoded = value.encode('utf8')
        self.write_varint(len(encoded))
        self.write(encoded)

    def write_chat(self, value):
        self.write_string(value)
    
    def write_identifier(self, value):
        self.write_string(value)

    def write_varint(self, value):
        if value < 0:
            value += 0x100000000
        count = 5
        while True:
            temp = value & 0b01111111
            value >>= 7
            if value != 0:
                temp |= 0b10000000
            self.write_byte(temp)
            if value == 0:
                break
            count -= 1
            if count <= 0:
                raise Exception('Value too large for varint')
    
    def write_varlong(self, value):
        if value < 0:
            value += 0x10000000000000000
        count = 10
        while True:
            temp = value & 0b01111111
            value >>= 7
            if value != 0:
                temp |= 0b10000000
            self.write_byte(temp)
            if value == 0:
                break
            count -= 1
            if count <= 0:
                raise Exception('Value too large for varlong')

    def write_position(self, x, y, z):
        self.write_long(((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF))

    def write_angle(self, value):
        self.write_byte(int(value * 256))

    def write_uuid(self, value):
        self.write(value.bytes)

    def write_byte_array(self, value):
        self.write(value)
