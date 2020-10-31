from mc_client.io.data_reader import read_varint

class SetCompression:
    def __init__(self, threshold):
        self.threshold = threshold

    def __repr__(self):
        return f'SetCompression(threshold={self.threshold})'

    @staticmethod
    def read_packet(reader):
        threshold = read_varint(reader)
        return SetCompression(threshold)
