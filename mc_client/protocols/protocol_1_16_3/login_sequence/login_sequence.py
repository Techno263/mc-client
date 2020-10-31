from ..clientbound.login import Disconnect, EncryptionRequest, LoginSuccess, SetCompression, LoginPluginRequest, PacketID as LoginPacketID
from ..serverbound.handshaking import Handshake
from mc_client.io.packet_io import write_uncompressed_packet, write_compressed_packet, read_uncompressed_packet, read_compressed_packet
from mc_client.protocols.protocol_1_16_3.serverbound.login import LoginStart
from mc_client.net.connection_state import ConnectionState
from mc_client.net.compression_state import CompressionState

def login_sequence(net_manager, socket_reader, socket_writer, host, port, name):
    write_uncompressed_packet(socket_writer, Handshake(753, host, port, ConnectionState.Login))
    net_manager.connection_state = ConnectionState.Login
    write_uncompressed_packet(socket_writer, LoginStart(name))
    socket_writer.flush()
    while net_manager.connection_state == ConnectionState.Login:
        _login_packet_handler(net_manager, socket_reader, socket_writer)

def _login_packet_handler(net_manager, socket_reader, socket_writer):
    if net_manager.compression_state == CompressionState.Compressed:
        packet_id, data_buffer, data_length = read_compressed_packet(socket_reader)
    else:
        packet_id, data_buffer, data_length = read_uncompressed_packet(socket_reader)
    if packet_id == LoginPacketID.Disconnect:
        disconnect = Disconnect.read_packet(data_buffer)
        print(disconnect)
    elif packet_id == LoginPacketID.EncryptionRequest:
        encryption_request = EncryptionRequest.read_packet(data_buffer)
        print(encryption_request)
    elif packet_id == LoginPacketID.LoginSuccess:
        login_success = LoginSuccess.read_packet(data_buffer)
        net_manager.connection_state = ConnectionState.Play
        print(login_success)
    elif packet_id == LoginPacketID.SetCompression:
        set_compression = SetCompression.read_packet(data_buffer)
        net_manager.compression_threshold = set_compression.threshold
        net_manager.compression_state = CompressionState.Compressed
        print(set_compression)
    elif packet_id == LoginPacketID.LoginPluginRequest:
        login_plugin_request = LoginPluginRequest.read_packet(data_buffer, -1)
        print(login_plugin_request)