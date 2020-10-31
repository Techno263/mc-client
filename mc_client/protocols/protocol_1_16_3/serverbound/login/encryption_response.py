from .packet_id import PacketID
from mc_client.io.data_writer import write_varint, write_byte_array

class EncryptionResponse:
    def __init__(self, shared_secret, verify_token):
        self.shared_secret = shared_secret
        self.verify_token = verify_token

    def write_packet(self, writer):
        write_varint(writer, PacketID.EncryptionResponse)
        write_varint(writer, len(self.shared_secret))
        write_byte_array(writer, self.shared_secret)
        write_varint(writer, len(self.verify_token))
        write_byte_array(writer, self.verify_token)
