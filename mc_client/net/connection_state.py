from enum import IntEnum

class ConnectionState(IntEnum):
    Handshake = 0
    Status = 1
    Login = 2
    Play = 3