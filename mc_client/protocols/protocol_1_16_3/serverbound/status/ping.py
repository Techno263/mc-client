from .packet_id import PacketID
from mc_client.io.data_writer import write_varint, write_long

class Ping():
    def __init__(self, payload):
        self.payload = payload

    def write_packet(self, writer):
        write_varint(writer, PacketID.Ping)
        write_long(writer, self.payload)