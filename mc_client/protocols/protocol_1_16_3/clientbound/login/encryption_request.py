from mc_client.io.data_reader import read_string, read_varint, read_byte_array

class EncryptionRequest:
    def __init__(self, server_id,
                 public_key, verify_token):
        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token
    
    def __repr__(self):
        return f'EncryptionRequest(server_id={self.server_id}, public_key={self.public_key}, verify_token={self.verify_token})'

    @staticmethod
    def read_packet(reader):
        server_id = read_string(reader)
        public_key_length = read_varint(reader)
        public_key = read_byte_array(reader, public_key_length)
        verify_token_length = read_varint(reader)
        verify_token = read_byte_array(reader, verify_token_length)
        return EncryptionRequest(server_id, public_key, verify_token)
