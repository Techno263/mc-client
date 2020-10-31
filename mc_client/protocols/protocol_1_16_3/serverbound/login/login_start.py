from io import BytesIO
from .packet_id import PacketID
from mc_client.io.datatype_length import varint_length, string_length
from mc_client.io.data_writer import write_varint, write_string

class LoginStart:
    def __init__(self, name):
        self.name = name

    def __len__(self):
        return varint_length(PacketID.LoginStart) + \
               string_length(self.name)

    def __bytes__(self):
        buffer = BytesIO()
        self.write_packet(buffer)
        buffer.seek(0, 0)
        return buffer.read()

    def write_packet(self, writer):
        write_varint(writer, PacketID.LoginStart)
        write_string(writer, self.name)
