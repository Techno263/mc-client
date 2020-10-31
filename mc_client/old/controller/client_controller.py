from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from mc_client.datatypes.data_reader import DataReader
from mc_client.datatypes.data_writer import DataWriter
from mc_client.protocols.protocol_1_16_3.serverbound.handshaking.handshake import Handshake 
from mc_client.protocols.protocol_1_16_3.serverbound.login.login_start import LoginStart
from mc_client.protocols.protocol_1_16_3.clientbound.login.encryption_request import EncryptionRequest

import time

class ClientController():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))
        self.data_reader = DataReader(self.socket.makefile('rb'))
        self.data_writer = DataWriter(self.socket.makefile('wb'))

    def read_packet(self):
        packet_len = self.data_reader.read_varint()
        packet_id = self.data_reader.read_varint()
        return packet_id, packet_len

    def start_login(self):
        Handshake(753, '127.0.0.1', 25565, 2).write_packet(self.data_writer)
        LoginStart('Bot_Test').write_packet(self.data_writer)
        self.data_writer.writer.flush()
        encrypt_req = EncryptionRequest.read_packet(self.data_reader)
        print(encrypt_req)
