from mc_client.io.data_reader import read_chat

class Disconnect:
    def __init__(self, reason):
        self.reason = reason
    
    def __repr__(self):
        return f'Disconnect(reason={self.reason})'

    @staticmethod
    def read_packet(reader):
        reason = read_chat(reader)
        return Disconnect(reason)
