from mc_client.io.data_reader import read_uuid, read_string

class LoginSuccess:
    def __init__(self, uuid, username):
        self.uuid = uuid
        self.username = username

    def __repr__(self):
        return f'LoginSuccess(uuid={self.uuid}, username={self.username})'

    @staticmethod
    def read_packet(reader):
        uuid = read_uuid(reader)
        username = read_string(reader)
        return LoginSuccess(uuid, username)
