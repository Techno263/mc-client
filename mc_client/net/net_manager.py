from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from ..io.packet_io import write_uncompressed_packet, write_compressed_packet, read_uncompressed_packet, read_compressed_packet
from ..protocols.protocol_1_16_3.serverbound.handshaking import Handshake
from ..protocols.protocol_1_16_3.serverbound.login import LoginStart
from ..protocols.protocol_1_16_3.clientbound.login import Disconnect, EncryptionRequest, LoginSuccess, SetCompression, LoginPluginRequest, PacketID as LoginPacketID
from ..io.datatype_length import varint_length
from ..net.connection_state import ConnectionState
from ..net.compression_state import CompressionState

class NetManager:
    def __init__(self, login_sequence):
        self.connection_state = ConnectionState.Handshake
        self.compression_state = CompressionState.NotCompressed
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket_reader = self.socket.makefile('rb')
        self.socket_writer = self.socket.makefile('wb')
        self.login_sequence = login_sequence
        self.listen_thread = Thread(target=NetManager._listen_thread, args=(self.socket_reader, ))

    def connect(self, host, port, name):
        self.socket.connect((host, port))
        self.login_sequence(self, self.socket_reader, self.socket_writer, host, port, name)
        assert self.connection_state == ConnectionState.Play

    def close(self):
        self.socket.close()
        self.socket_reader.close()
        self.socket_writer.close()

    @staticmethod
    def _listen_thread(socket_reader, packet_handler):
        pass
