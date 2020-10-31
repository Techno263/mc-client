from struct import unpack
from uuid import UUID
from .nbt import parse_nbt

def read_boolean(reader):
    return bool(unpack('>B', reader.read(1))[0])

def read_sbyte(reader):
    return unpack('>b', reader.read(1))[0]

def read_byte(reader):
    return unpack('>B', reader.read(1))[0]

def read_short(reader):
    return unpack('>h', reader.read(2))[0]

def read_ushort(reader):
    return unpack('>H', reader.read(2))[0]

def read_int(reader):
    return unpack('>i', reader.read(4))[0]

def read_long(reader):
    return unpack('>q', reader.read(8))[0]

def read_float(reader):
    return unpack('>f', reader.read(4))[0]

def read_double(reader):
    return unpack('>d', reader.read(8))[0]

def read_string(reader):
    length = read_varint(reader)
    string = reader.read(length).decode('utf8')
    return string

def read_chat(reader):
    return read_string(reader)

def read_identifier(reader):
    return read_string(reader)

def read_varint(reader):
    num_read = 0
    result = 0
    while True:
        read = read_byte(reader)
        value = read & 0b01111111
        result |= value << (7 * num_read)
        num_read += 1
        if num_read > 5:
            raise Exception('VarInt is too large')
        if read & 0b10000000 == 0:
            break
    return result

def read_varlong(reader):
    num_read = 0
    result = 0
    while True:
        read = read_byte(reader)
        value = read & 0b01111111
        result |= value << (7 * num_read)
        num_read += 1
        if num_read > 10:
            raise Exception('VarLong is too large')
        if read & 0b10000000 == 0:
            break
    return result

def _read_particle(reader):
    particle_id = read_varint(reader)
    if particle_id == 3:
        return particle_id, read_varint(reader)
    elif particle_id == 14:
        return particle_id, read_float(reader), read_float(reader), read_float(reader), read_float(reader)
    elif particle_id == 23:
        return particle_id, read_varint(reader)
    elif particle_id == 32:
        return particle_id, read_slot(reader)
    else:
        return particle_id,

def _read_entity_metadata_element(reader):
    value_type = read_varint(reader)
    if value_type == 0:
        return read_byte(reader)
    elif value_type == 1:
        return read_varint(reader)
    elif value_type == 2:
        return read_float(reader)
    elif value_type == 3:
        return read_string(reader)
    elif value_type == 4:
        return read_chat(reader)
    elif value_type == 5:
        if read_boolean(reader):
            return read_chat(reader)
        else:
            return None
    elif value_type == 6:
        return read_slot(reader)
    elif value_type == 7:
        return read_boolean(reader)
    elif value_type == 8:
        return (read_float(reader), read_float(reader), read_float(reader))
    elif value_type == 9:
        return read_position(reader)
    elif value_type == 10:
        if read_boolean(reader):
            return read_position(reader)
        else:
            return None
    elif value_type == 11:
        return read_varint(reader)
    elif value_type == 12:
        if read_boolean(reader):
            return read_uuid(reader)
        else:
            return None
    elif value_type == 13:
        return read_varint(reader)
    elif value_type == 14:
        return read_nbt(reader)
    elif value_type == 15:
        return _read_particle(reader)


def read_entity_metadata(reader):
    index = read_byte(reader)
    if index != 0xff:
        value_type = read_varint(reader)
        if value_type == 0:
            return read_byte(reader)
        elif value_type == 1:
            return read_varint(reader)
        elif value_type == 2:
            return read_float(reader)
        elif value_type == 3:
            return read_string(reader)
        elif value_type == 4:
            return read_chat(reader)
        elif value_type == 5:
            if read_boolean(reader):
                return read_chat(reader)
            else:
                return None
        elif value_type == 6:
            return read_slot(reader)
        elif value_type == 7:
            return read_boolean(reader)
        elif value_type == 8:
            return read_float(reader), read_float(reader), read_float(reader)
        elif value_type == 9:
            return read_position(reader)
        elif value_type == 10:
            if read_boolean(reader):
                return read_position(reader)
            else:
                return None
        elif value_type == 11:
            return read_varint(reader)
        elif value_type == 12:
            if read_boolean(reader):
                return read_uuid(reader)
            else:
                return None
        elif value_type == 13:
            if read_boolean(reader):
                return read_varint(reader)
            else:
                return None
        elif value_type == 14:
            return read_nbt(reader)
        elif value_type == 15:
            return _read_particle(reader)
        elif value_type == 16:
            return read_varint(reader)
        elif value_type == 17:
            if read_boolean(reader):
                return read_varint(reader)
            else:
                return None
        elif value_type == 18:
            return read_varint(reader)
        else:
            raise Exception('Invalid entity metadata type')

def read_slot(reader):
    return read_nbt(reader)

def read_nbt(reader):
    return parse_nbt(reader)

def read_position(reader):
    value = read_long(reader)
    x = (value & (0x3FFFFFF << 38)) >> 38
    y = value & 0xFFF
    z = (value & (0x3FFFFFF << 12)) >> 12
    return x, y, z

def read_angle(reader):
    return read_byte(reader) / 256

def read_uuid(reader):
    return UUID(bytes=reader.read(16))

def read_array(reader):
    raise Exception('Not impemented')

def read_byte_array(reader, length):
    return reader.read(length)
