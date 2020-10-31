

class PacketReader():
    def __init__(self, reader, parse_dict):
        self.reader = reader
        self.parse_dict = parse_dict
        self.has_set_compression = False

    def set_compression(self):
        self.has_set_compression = True

    def parse_packet(self):
        if self.has_set_compression:
            pass
        else:
            length = self.reader.read_varint()
            packet_id = self.read.read_varint()