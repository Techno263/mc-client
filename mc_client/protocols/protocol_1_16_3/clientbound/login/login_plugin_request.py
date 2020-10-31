from mc_client.io.data_reader import read_varint, read_identifier, read_byte_array

class LoginPluginRequest:
    def __init__(self, message_id, channel, data):
        self.message_id = message_id
        self.channel = channel
        self.data = data

    def __repr__(self):
        return f'LoginPluginRequest(message_id={self.message_id}, channel={self.channel}, data={self.data})'

    @staticmethod
    def read_packet(reader, data_len):
        message_id = read_varint(reader)
        channel = read_identifier(reader)
        data = read_byte_array(reader, data_len)
        return LoginPluginRequest(message_id, channel, data)
