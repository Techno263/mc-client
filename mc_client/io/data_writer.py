from struct import pack
from uuid import UUID

def write_boolean(writer, value):
    if not isinstance(bool, value):
        value = bool(value)
    writer.write(pack('>B', value))

def write_sbyte(writer, value):
    writer.write(pack('>b', value))

def write_byte(writer, value):
    writer.write(pack('>B', value))

def write_short(writer, value):
    writer.write(pack('>h', value))

def write_ushort(writer, value):
    writer.write(pack('>H', value))

def write_int(writer, value):
    writer.write(pack('>i', value))

def write_long(writer, value):
    writer.write(pack('>q', value))

def write_float(writer, value):
    writer.write(pack('>f', value))

def write_double(writer, value):
    writer.write(pack('>d', value))

def write_string(writer, value):
    encoded = value.encode('utf8')
    write_varint(writer, len(encoded))
    writer.write(encoded)

def write_chat(writer, value):
    write_string(writer, value)

def write_identifier(writer, value):
    write_string(writer, value)

def write_varint(writer, value):
    if value < 0:
        value += 0x100000000
    count = 5
    while True:
        temp = value & 0b01111111
        value >>= 7
        if value != 0:
            temp |= 0b10000000
        write_byte(writer, temp)
        if value == 0:
            break
        count -= 1
        if count <= 0:
            raise Exception('Value too large for varint')

def write_varlong(writer, value):
    if value < 0:
        value += 0x10000000000000000
    count = 10
    while True:
        temp = value & 0b01111111
        value >>= 7
        if value != 0:
            temp |= 0b10000000
        write_byte(writer, temp)
        if value == 0:
            break
        count -= 1
        if count <= 0:
            raise Exception('Value too large for varlong')

def write_position(writer, x, y, z):
    write_long(writer, ((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF))

def write_angle(writer, value):
    write_byte(writer, int(value * 256))

def write_uuid(writer, value):
    writer.write(value.bytes)

def write_byte_array(writer, value):
    writer.write(value)
