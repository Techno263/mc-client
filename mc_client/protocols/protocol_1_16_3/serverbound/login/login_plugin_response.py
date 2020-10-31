from .packet_id import PacketID
from mc_client.io.data_writer import write_varint, write_boolean, write_byte_array

class LoginPluginResponse:
    def __init__(self, message_id, successful, data):
        self.message_id = message_id
        self.successful = successful
        self.data = data

    def write_packet(self, writer):
        write_varint(writer, PacketID.LoginPluginResponse)
        write_varint(writer, self.message_id)
        write_boolean(writer, self.successful)
        write_byte_array(writer, self.data)
