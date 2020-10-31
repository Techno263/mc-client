from .packet_id import PacketID
from mc_client.io.data_writer import write_varint

class Request():
    def __init__(self):
        pass

    def write_packet(self, writer):
        write_varint(writer, PacketID.Request)