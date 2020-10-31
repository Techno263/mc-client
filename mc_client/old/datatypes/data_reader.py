import struct
from io import BufferedReader, DEFAULT_BUFFER_SIZE
from uuid import UUID
from .nbt import parse_nbt

class DataReader():
    def __init__(self, reader):
        self.reader = reader

    def read(self, size=-1):
        return self.reader.read(size)

    def read_boolean(self):
        return bool(struct.unpack('>B', self.read(1))[0])

    def read_sbyte(self):
        return struct.unpack('>b', self.read(1))[0]

    def read_byte(self):
        return struct.unpack('>B', self.read(1))[0]
    
    def read_short(self):
        return struct.unpack('>h', self.read(2))[0]
    
    def read_ushort(self):
        return struct.unpack('>H', self.read(2))[0]

    def read_int(self):
        return struct.unpack('>i', self.read(4))[0]

    def read_long(self):
        return struct.unpack('>q', self.read(8))[0]

    def read_float(self):
        return struct.unpack('>f', self.read(4))[0]

    def read_double(self):
        return struct.unpack('>d', self.read(8))[0]

    def read_string(self):
        length = self.read_varint()
        string = self.read(length).decode('utf8')
        return string

    def read_chat(self):
        return self.read_string()

    def read_identifier(self):
        return self.read_string()

    def read_varint(self):
        num_read = 0
        result = 0
        while True:
            read = self.read_byte()
            value = read & 0b01111111
            result |= value << (7 * num_read)
            num_read += 1
            if num_read > 5:
                raise Exception('VarInt is too large')
            if read & 0b10000000 == 0:
                break
        return result

    def read_varlong(self):
        num_read = 0
        result = 0
        while True:
            read = self.read_byte()
            value = read & 0b01111111
            result |= value << (7 * num_read)
            num_read += 1
            if num_read > 10:
                raise Exception('VarLong is too large')
            if read & 0b10000000 == 0:
                break
        return result

    def _read_particle(self):
        particle_id = self.read_varint()
        if particle_id == 3:
            return particle_id, self.read_varint()
        elif particle_id == 14:
            return particle_id, self.read_float(), self.read_float(), self.read_float(), self.read_float()
        elif particle_id == 23:
            return particle_id, self.read_varint()
        elif particle_id == 32:
            return particle_id, self.read_slot()
        else:
            return particle_id,

    def _read_entity_metadata_element(self):
        value_type = self.read_varint()
        if value_type == 0:
            return self.read_byte()
        elif value_type == 1:
            return self.read_varint()
        elif value_type == 2:
            return self.read_float()
        elif value_type == 3:
            return self.read_string()
        elif value_type == 4:
            return self.read_chat()
        elif value_type == 5:
            if self.read_boolean():
                return self.read_chat()
            else:
                return None
        elif value_type == 6:
            return self.read_slot()
        elif value_type == 7:
            return self.read_boolean()
        elif value_type == 8:
            return (self.read_float(), self.read_float(), self.read_float())
        elif value_type == 9:
            return self.read_position()
        elif value_type == 10:
            if self.read_boolean():
                return self.read_position()
            else:
                return None
        elif value_type == 11:
            return self.read_varint()
        elif value_type == 12:
            if self.read_boolean():
                return self.read_uuid()
            else:
                return None
        elif value_type == 13:
            return self.read_varint()
        elif value_type == 14:
            return self.read_nbt()
        elif value_type == 15:
            return self._read_particle()


    def read_entity_metadata(self):
        index = self.read_byte()
        if index != 0xff:
            value_type = self.read_varint()
            if value_type == 0:
                return self.read_byte()
            elif value_type == 1:
                return self.read_varint()
            elif value_type == 2:
                return self.read_float()
            elif value_type == 3:
                return self.read_string()
            elif value_type == 4:
                return self.read_chat()
            elif value_type == 5:
                if self.read_boolean():
                    return self.read_chat()
                else:
                    return None
            elif value_type == 6:
                return self.read_slot()
            elif value_type == 7:
                return self.read_boolean()
            elif value_type == 8:
                return self.read_float(), self.read_float(), self.read_float()
            elif value_type == 9:
                return self.read_position()
            elif value_type == 10:
                if self.read_boolean():
                    return self.read_position()
                else:
                    return None
            elif value_type == 11:
                return self.read_varint()
            elif value_type == 12:
                if self.read_boolean():
                    return self.read_uuid()
                else:
                    return None
            elif value_type == 13:
                if self.read_boolean():
                    return self.read_varint()
                else:
                    return None
            elif value_type == 14:
                return self.read_nbt()
            elif value_type == 15:
                return self._read_particle()
            elif value_type == 16:
                return self.read_varint()
            elif value_type == 17:
                if self.read_boolean():
                    return self.read_varint()
                else:
                    return None
            elif value_type == 18:
                return self.read_varint()
            else:
                raise Exception('Invalid entity metadata type')

    def read_slot(self):
        return self.read_nbt()

    def read_nbt(self):
        return parse_nbt(self)

    def read_position(self):
        value = self.read_long()
        x = (value & (0x3FFFFFF << 38)) >> 38
        y = value & 0xFFF
        z = (value & (0x3FFFFFF << 12)) >> 12
        return x, y, z

    def read_angle(self):
        return self.read_byte() / 256

    def read_uuid(self):
        return UUID(bytes=self.read(16))

    def read_array(self):
        raise Exception('Not impemented')

    def read_byte_array(self, length):
        return self.read(length)
