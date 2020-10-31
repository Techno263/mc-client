from io import BytesIO
from .packet_id import PacketID
from mc_client.io.datatype_length import varint_length, string_length, ushort_length
from mc_client.io.data_writer import write_varint, write_string, write_ushort

class Handshake:
    def __init__(self, protocol_version, server_address, server_port, next_state):
        self.protocol_version = protocol_version
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

    def __len__(self):
        return varint_length(PacketID.Handshake) + \
               varint_length(self.protocol_version) + \
               string_length(self.server_address) + \
               ushort_length() + \
               varint_length(self.next_state)

    def __bytes__(self):
        buffer = BytesIO()
        self.write_packet(buffer)
        buffer.seek(0, 0)
        return buffer.read()

    def write_packet(self, writer):
        write_varint(writer, PacketID.Handshake)
        write_varint(writer, self.protocol_version)
        write_string(writer, self.server_address)
        write_ushort(writer, self.server_port)
        write_varint(writer, self.next_state)
