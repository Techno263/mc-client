from struct import pack, unpack
from zlib import decompress, compress
from io import BytesIO
from .data_reader import read_varint
from .data_writer import write_varint, write_byte_array
from .datatype_length import varint_length

def read_uncompressed_packet(reader):
    length = read_varint(reader)
    data_buffer = BytesIO(reader.read(length))
    packet_id = read_varint(data_buffer)
    return packet_id, data_buffer, length - varint_length(packet_id)

def read_compressed_packet(reader):
    packet_length = read_varint(reader)
    data_buffer = BytesIO(reader.read(packet_length))
    data_length = read_varint(data_buffer)
    if data_length != 0:
        data_buffer = BytesIO(decompress(data_buffer.read()))
    else:
        data_length = packet_length
    packet_id = read_varint(data_buffer)
    return packet_id, data_buffer, data_length - varint_length(packet_id)

def write_uncompressed_packet(writer, packet):
    write_varint(writer, len(packet))
    packet.write_packet(writer)

def write_compressed_packet(writer, packet):
    data_length = len(packet)
    data = compress(bytes(packet))
    write_varint(writer, varint_length(data_length) + len(data))
    write_varint(writer, data_length)
    write_byte_array(writer, data)
