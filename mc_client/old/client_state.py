from enum import IntEnum

class ClientState(IntEnum):
    Handshaking = 0
    Status = 1
    Login = 2
    Play = 3
