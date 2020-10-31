from mc_client.io.data_reader import read_string

class Response:
    def __init__(self, response):
        self.response = response

    @staticmethod
    def read_packet(reader):
        response = read_string(reader)
        return Response(response)
