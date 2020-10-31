from mc_client.io.data_reader import read_long

class Pong:
    def __init__(self, payload):
        self.payload = payload

    @staticmethod
    def read_packet(reader):
        payload = read_long(reader)
        return Pong(payload)
